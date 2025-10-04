import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-auth-practice',
  imports: [CommonModule],
  standalone:true,
  templateUrl: './auth-practice.html',
  styleUrl: './auth-practice.css'
})
export class AuthPractice {

  activePanel='login';

  setActive(panel:string){
    return this.activePanel=panel;

  }

  onLogin(username:string,password:string){
    if(!username||!password){
      alert('Enter username&password')
      return;
    }
    alert(`Logging in with ${username}`);
  }

  onSignup(username: string, email: string, password: string){
    if(!username||!password || !email){
      alert('Enter username&password')
      return;
    }
    alert(`Logging in with ${username}`);
  }

}
