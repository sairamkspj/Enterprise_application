import { Routes } from '@angular/router';
import { Welcome } from './welcome/welcome';
import { Registration } from './registration/registration';
import { Login } from './login/login';
import { DashboardComp } from './dashboard-comp/dashboard-comp';
import { Auth } from './auth/auth';
import { AuthPractice } from './auth-practice/auth-practice';
import { PracticeCss } from './practice-css/practice-css';
import { LogUploadComponent } from './log-file/log-file';


export const routes: Routes =  [
  { path: '', component: Registration },            // default = Registration form
  { path: 'registration', component: Registration }, // also accessible by /registration
  { path: 'welcome', component: Welcome },
  { path: 'login', component:Login},
  { path: 'dashboard', component:DashboardComp},
  { path: 'auth',component:Auth},
  { path: 'authpractice',component:AuthPractice},
  {path:'cssprac',component:PracticeCss},
  {path:'log',component:LogUploadComponent}

];