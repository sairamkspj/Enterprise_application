

import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient,withFetch} from '@angular/common/http';
import { AppComponent } from './app/app';
import { routes } from './app/app.routes'
import { provideRouter } from '@angular/router';

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(withFetch()),
    provideRouter(routes)   // ✅ replaces HttpClientModule
  ],
}).catch(err => console.error(err));

// | Feature               | CSR (`ng serve`)                            | SSR (`ng serve --ssr`)                  |
// | --------------------- | ------------------------------------------- | --------------------------------------- |
// | Entry point           | `main.ts`                                   | `main.server.ts` + `main.ts`            |
// | Server work           | Minimal → only sends empty HTML + JS bundle | Server runs Angular, renders HTML fully |
// | Browser work          | Runs Angular to build UI                    | Only hydrates (activates interactivity) |
// | First content visible | After Angular finishes → slower             | Immediately → faster first paint        |
// | SEO                   | Weak (empty HTML initially)                 | Strong (server-sent HTML)               |
// | Use case              | Dashboards, internal apps                   | E-commerce, blogs, SEO-focused apps     |


// 1️⃣ Browser requests URL: /registration
//    |
//    v
// 2️⃣ Server receives request and bootstraps Angular (SSR)
//    bootstrapApplication(AppComponent, {
//      providers: [provideHttpClient(), provideRouter(routes)]
//    })
//    |
//    v
// 3️⃣ Server matches route → Registration component
//    - Instantiates Registration component
//    - DI resolves RegistrationService
//    - DI resolves HttpClient (required for service)
//    |
//    v
// 4️⃣ Server renders HTML
//    <app-root>
//      <p>registration works!</p>
//      <form>
//        <input name="Name" value="">
//        <input name="Email" value="">
//        <input name="Password" value="">
//        <select name="Role">...</select>
//        <button type="submit">Submit</button>
//      </form>
//    </app-root>
//    <script src="main.js"></script>
//    |
//    v
// 5️⃣ Browser receives fully rendered HTML (first paint)
//    - User sees form immediately
//    - But ngModel, ngSubmit, and other directives not active yet
//    |
//    v
// 6️⃣ Browser downloads main.js
//    - Contains Angular runtime + components + services + directives
//    |
//    v
// 7️⃣ Angular bootstraps in browser (Hydration)
//    - Attaches component instances to existing DOM
//    - Activates all directives:
//        - [(ngModel)] binds input to component variables
//        - (ngSubmit) binds form submit to onSubmit()
//        - Structural directives (*ngIf, *ngFor) applied
//    - DI resolves services in browser if needed
//    |
//    v
// 8️⃣ Page fully interactive
//    - User types → component variable updates
//    - User submits → RegistrationService called with HttpClient
//    - Routing works


// | Step   | CSR only                                      | SSR + Hydration                                         |
// | ------ | --------------------------------------------- | ------------------------------------------------------- |
// | 0s     | Browser requests page                         | Browser requests page                                   |
// | 0.2s   | Server sends empty `index.html` + JS          | Server bootstraps Angular, instantiates components      |
// | 0.3–1s | Browser downloads JS, bootstraps AppComponent | Server renders full HTML                                |
// | 1–2s   | Angular renders Registration component        | Browser receives HTML → user sees page                  |
// | 2–3s   | Page becomes visible                          | Browser downloads JS (`main.js`)                        |
// | 3–4s   | Page interactive                              | Angular hydrates → attaches directives + event handlers |
// | 4s+    | Fully interactive                             | Page fully interactive                                  |
