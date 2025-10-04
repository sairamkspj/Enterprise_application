import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { LoginService } from './login_service';
import { HttpClient } from '@angular/common/http';
import { response } from 'express';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {
  Authentication:FormGroup;

  constructor(private fb:FormBuilder,private http:HttpClient,private login_service:LoginService,private router:Router){
    this.Authentication=this.fb.group({
      Username:[''],
      Password:['']
    })
  }

  onSubmit(){
    this.login_service.login(this.Authentication.value).subscribe({
      

      
      next: (response:any) =>{
        
        console.log('login success', response);
        
        if(response.roles.includes("Admin")){

          this.router.navigate(['/auth'])

        }
      },

      error: (response:any) =>{
        console.log('login unsuccess', response);
      },

      complete: () => {
          console.log('login request completed');
        }
    
  })
    console.log(this.Authentication.value)
  }


}
