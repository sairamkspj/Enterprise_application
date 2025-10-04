import { Component } from '@angular/core';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.html',
  styleUrls: ['./auth.css']
})
export class Auth {
  activePanel: 'login' | 'signup' = 'login'; // default view

  setActive(panel: 'login' | 'signup') {
    this.activePanel = panel;
  }

  onLogin(username: string, password: string) {
    if (!username || !password) {
      alert('Enter username & password');
      return;
    }
    // 🔗 Call Django backend login API here
    alert(`Logging in with ${username}`);
  }

  onSignup(username: string, email: string, password: string) {
    if (!username || !email || !password) {
      alert('Fill all fields');
      return;
    }
    // 🔗 Call Django backend signup API here
    alert(`Signing up ${username} (${email})`);
  }
}
