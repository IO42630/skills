---
name: com-olexyn-tabdriver
description: >
  Use when integrating, wiring, or modifying the com.olexyn:tabdriver browser-automation library
  in a JVM/Java app with any DI framework (Spring, Quarkus, or none) — shared TabDriver, config
  provider, Purpose tabs, TabDriverHolder, session login handling. Triggers on TabDriver, tabdriver,
  chromedriver, TabDriverHolder, TabDriverConfigProvider, Purpose, browser session.
---

# Integrating TabDriver

- `com.olexyn:tabdriver` (verified against 1.5.1) wraps Selenium `ChromeDriver`.
    - Adds named tabs (`Purpose`) and CSS-first finders that return `Optional` / empty list, never throw.
    - Uses Chrome only (`chromedriver`, not Chromium) and plain Java with no DI dependency.
    - Register the classes below as application-scoped singletons.
        - Spring `@Service`, Quarkus `@ApplicationScoped` / `@Singleton`, or a hand-rolled singleton.
- The integration has four parts.
    - `TabDriverConfigProvider` — supplies driver path, download dir, headless flag, `ChromeOptions`.
    - `TabDriverHolder` — exactly one `TabDriver` per JVM, created lazily.
    - A `Purpose` wrapper enum — names every tab.
    - `Session` navigators — own login, liveness, and page interaction per site.

## 1. Dependency

- Declare the version once in the parent `<dependencyManagement>`.
- Modules depend on it without a version.

```xml
<!-- root pom.xml -->
<dependency>
  <groupId>com.olexyn</groupId>
  <artifactId>tabdriver</artifactId>
  <version>1.5.1</version>
</dependency>

<!-- module pom.xml -->
<dependency>
  <groupId>com.olexyn</groupId>
  <artifactId>tabdriver</artifactId>
</dependency>
```

- TabDriver pulls in Selenium; no other browser dependency is needed.
- 1.5.1 targets **Java 25** and Selenium 4.49.
    - The consumer JVM must be Java 25+; older JVMs fail with `UnsupportedClassVersionError`.

## 2. Implement the config provider

- `TabDriver` is constructed from a `TabDriverConfigProvider` with four methods.
    - `getDriverPath()`, `getDownloadDir()`, `isHeadless()`, `getOptions()`.
- Extend `DefaultTabDriverConfig`; do not implement the interface from scratch.
    - The base builds `ChromeOptions`: accepts insecure certs and always adds `--start-maximized`.
    - In headless mode it also adds `--headless --window-size=1920,1080`.
    - It sets prefs: `download.default_directory`, `download.prompt_for_download=false`, popups off.
    - Override `getOptions()` only to add your own flags.
- Read the three host values from your configuration source; never hardcode.

```java
public class AppTabDriverConfig extends DefaultTabDriverConfig {

  private final Path driverPath;
  private final Path downloadDir;
  private final boolean headless;

  public AppTabDriverConfig(Path driverPath, Path downloadDir, boolean headless) {
    this.driverPath = driverPath;
    this.downloadDir = downloadDir;
    this.headless = headless;
  }

  @Override public Path getDriverPath() { return driverPath; }
  @Override public String getDownloadDir() { return downloadDir.toString(); }
  @Override public boolean isHeadless() { return headless; }
}
```

- `getDriverPath()` must point at an existing ChromeDriver executable; use an absolute path.
    - ChromeDriver's major version must match the installed Chrome.
    - On macOS clear the quarantine bit once: `xattr -dr com.apple.quarantine <chromedriver>`.
- There is no properties-file loader.
    - The README's `TabDriverBuilder` example is stale; that class was removed in 1.4.
    - Supply the values programmatically or via your own config framework.
- Config is consumed in the `TabDriver` constructor.
    - A missing driver path or download dir fails at first browser use, not at startup.
- `TabDriver` builds a `ChromeDriverService` on any free port; no port config is needed.
    - It sets a 2 s implicit wait itself.

## 3. Hold one shared TabDriver

- There must be exactly one `TabDriver` per JVM.
- The holder creates it lazily on first use under a private lock.
- `getOpt()` exposes it without triggering creation.

```java
public class TabDriverHolder {

  private final TabDriverConfigProvider tdConfig;
  private volatile TabDriver td = null;
  private final Object lock = new Object();

  public TabDriverHolder(TabDriverConfigProvider tdConfig) {
    this.tdConfig = tdConfig;
  }

  public TabDriver get() {
    synchronized (lock) {
      if (td == null) { td = new TabDriver(tdConfig); }
      return td;
    }
  }

  public Optional<TabDriver> getOpt() { return Optional.ofNullable(td); }
  public boolean isInit() { return td != null; }
}
```

- `td` is `volatile` so lock-free `getOpt()` / `isInit()` reads see a fully initialized driver.
- Do not instantiate raw `WebDriver` / `ChromeDriver` anywhere else; always go through the holder.
- Container notes:
    - Quarkus `@ApplicationScoped` is lazy through its client proxy.
    - Spring: declare the bean `@Lazy` or construct it by hand.
- `quit()` leaves `td` pointing at a dead driver; treat the holder as terminal after shutdown.

## 4. Name every tab with a Purpose

- `TabDriver` tracks tabs in a `Map<windowHandle, Tab>` and resolves them by `Purpose`.
- Wrap the enum once and reuse the `Purpose` instances.

```java
public enum TabPurpose {
  LOGIN, DOWNLOAD, OBSERVE, SUBMIT /* ... */;

  private static final Map<TabPurpose, Purpose> MAP = new HashMap<>();
  static {
    Arrays.stream(values()).forEach(tp -> MAP.put(tp, new Purpose(tp.name())));
  }
  public static Purpose getTabPurpose(TabPurpose tp) { return MAP.get(tp); }
}
```

- `newTab(Purpose)` is idempotent per purpose and leaves the new tab active.
    - It creates a window via `switchTo().newWindow(TAB)`; Chrome only.
    - If a tab with that purpose already exists it no-ops — it does not navigate to it.
- `goToTab(Purpose)` switches to the first matching tab and silently no-ops if none matches.
- Equality is by purpose name: a fresh `Purpose("X")` still matches an existing `Purpose("X")`.
    - The singleton map is just an allocation optimization.

## 5. Synchronize all browser access on `td`

- Most `TabDriver` methods are `synchronized` on the instance — the same monitor as `synchronized (td)`.
    - Synchronized: `newTab`, `goToTab`, `refresh`, `get`, every `find*`, `getByText`,
      `sendDeleteKeys`, `followContainedLink`, `setRadio`, `setComboByDataValue`, `executeScript(String)`.
- These are **not** synchronized: `navigate()`, `switchTo()`, `getWindowHandle()`,
  `getWindowHandles()`, `getTitle()`, `getCurrentUrl()`, `getPageSource()`, `close()`, `quit()`.
    - Prefer `td.refresh()` / `td.get(url)` over `navigate()`.
- Compound find-click sequences are not atomic; guard each sequence with `synchronized (td)`.

```java
synchronized (td) {
  td.goToTab(getTabPurpose(OBSERVE));
  WebElement row = td.findByCss("[data-id*='%s']".formatted(id)).orElseThrow();
  row.click();
}
```

- Keep sections short.
    - Never hold `td` across a `sleep`, a network wait, or while acquiring another lock.
    - Do not acquire a second monitor while holding `td`.
    - `get()` / `refresh()` do block under the monitor while the page loads; that is expected.

## 6. Model sessions, not just tabs

- For sites that require login, add a `Session` that detects liveness and waits for a human login.
    - It owns the `td` reference.
    - `cancelled` is any `BooleanSupplier` your app already has (job state, shutdown flag, `AtomicBoolean`).

```java
public abstract class Session {
  public final TabDriver td;
  private volatile boolean loggedIn = false;

  protected Session(TabDriver td) { this.td = td; }

  public abstract void doLogin(BooleanSupplier cancelled) throws InterruptedException;
  public boolean isSessionAlive() { return loggedIn; }
  public boolean isLoggedIn() { return loggedIn; }
  protected void setLoggedIn(boolean value) { this.loggedIn = value; }

  public void ensureLoggedIn(BooleanSupplier cancelled) throws InterruptedException {
    while (!cancelled.getAsBoolean()) {
      synchronized (td) {
        if (isSessionAlive()) { setLoggedIn(true); return; }
      }
      Thread.sleep(2000);
    }
    setLoggedIn(false);
  }
}
```

- The base `isSessionAlive()` consults `loggedIn`; a DOM-probe override ignores it,
  so `isLoggedIn()` stays useful as bookkeeping.
- Subclasses override `isSessionAlive()` with a DOM probe, open the login URL in `doLogin`,
  then call `ensureLoggedIn`.

```java
@Override
public boolean isSessionAlive() {
  synchronized (td) { return td.findByCss("button[class*=Account]").isPresent(); }
}

@Override
public void doLogin(BooleanSupplier cancelled) throws InterruptedException {
  synchronized (td) {
    if (isSessionAlive()) return;
    td.newTab(getTabPurpose(LOGIN));
    td.get("https://example.com/login");
  }
  ensureLoggedIn(cancelled);
}
```

- Interactive login needs a visible browser.
    - Headless runs cannot wait for a human; seed cookies/profile or keep a headful mode.
- Load credentials from an external file or secret store referenced by config — never inline secrets.

## 7. Navigator construction

- Navigators extend the platform `Session` and take the holder; pass `tdh.get()` to `super`.
- Register them as singletons if the container manages them.

```java
public class ExampleNavigator extends ExampleSession {
  public ExampleNavigator(TabDriverHolder tdh) {
    super(tdh.get());
  }
}
```

- `ITabDriver` is the narrow seam for callers that only need `newTab` / `goToTab`.
- Useful `TabDriver` API:
    - `findByCss(String)` / `findByCss(WebElement ctx, String)` → `Optional<WebElement>`
    - `findAllByCss(String)` / `findAllByCss(WebElement ctx, String)` → `List<WebElement>` (empty on missing)
    - `findByCssAndText(css, text)` → `Optional<WebElement>` (matches `textContent` containing `text`)
    - `getByText(String)` → XPath contains-text lookup
    - `sendDeleteKeys(WebElement, n)` — sends `n` backspaces
    - `setComboByDataValue(WebElement, String)` — clicks the combo, then `li[data-value='...']`
    - `followContainedLink(WebElement)` — navigates to the element's `href`
    - `refresh()`, `get(url)`, `navigate()`, `switchTo()`, `getPageSource()`,
      `getCurrentUrl()`, `getTitle()`, `getWindowHandle()`, `getWindowHandles()`
    - `newTab(Purpose)`, `goToTab(Purpose)`, `close()`, `quit()`
- Interact with elements through Selenium's native methods (`element.click()`, `element.sendKeys(...)`).
    - `TabDriver.click(...)`, `TabDriver.setRadio(...)`, and the `executeScript` family are silent no-ops in 1.5.1.

## 8. Lifecycle

- Close the browser on shutdown; use `getOpt()` so you never create a browser just to close it.
    - A JVM shutdown hook is the framework-agnostic default.
    - A control/API endpoint can call the same method on demand.
- In containers prefer lifecycle callbacks: Spring `@PreDestroy`, Quarkus `@PreDestroy` / `@Observes Shutdown`.

```java
Runtime.getRuntime().addShutdownHook(new Thread(
  () -> holder.getOpt().ifPresent(TabDriver::quit)
));
```

## 9. Gotchas

- **JavaScript is broken in 1.5.1.**
    - `executeScript(String, Object...)` and `executeAsyncScript(...)` are stubs returning `null`.
    - `TabDriver.executeScript(String)`, `click(WebElement)`, and `setRadio(WebElement, boolean)`
      all route into that stub, so they silently do nothing.
    - Use native `element.click()` / `element.sendKeys(...)`, and re-check these before relying on
      them in a later version.
- The `findByCss` / `findAllByCss` variants swallow every exception.
    - A dead session looks identical to "element missing".
    - Check session liveness separately when a missing element is suspicious.
    - `findByCssAndText` is the exception: it calls the raw `findElements` and can throw on a bad
      selector or dead session.
- `Purpose` is a record whose `equals` compares `name` only; the generated `hashCode` uses the
  same component, so the two stay consistent.
    - Prefer the singleton map, but equal-name instances still match.
- A tab's purpose is fixed at creation; reusing a window for another purpose silently keeps
  the old purpose.
- Tabs closed manually or by the site stay in the internal map.
    - `goToTab` no-ops and `newTab` will not recreate them.
- `getByText` interpolates text into an XPath expression without escaping; prefer
  `findByCss` / `findByCssAndText`.
- `setComboByDataValue` interpolates the value into a CSS selector without escaping;
  values containing `'` break it.
- Missing driver path / download dir config fails at first browser use, not at startup.
- Elements parsed from the page are unreliable; validate text/values before publishing them
  to the rest of the app, and keep CSS selectors easy to update.
