import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { FormBuilder,Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { login_reg_Service } from './service';

@Component({
  selector: 'app-practice-css',
  standalone:true,
  imports: [FormsModule,CommonModule,ReactiveFormsModule],
  templateUrl: './practice-css.html',
  styleUrl: './practice-css.css'
})
export class PracticeCss implements OnInit {
  activePanel: 'login' | 'signup' = 'login';
  
  loginForm!: FormGroup;
  signupForm!: FormGroup;

  constructor(private fb: FormBuilder,private service: login_reg_Service) {}


  ngOnInit(): void {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });

    this.signupForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  setActive(panel: 'login' | 'signup') {
    this.activePanel = panel;
  }

  onLoginSubmit() {
    if (this.loginForm.valid) {
      console.log('Login Data', this.loginForm.value);
      // call login API
    }
  }

  onSignupSubmit() {

    if (this.signupForm.valid) {
      console.log('signup Data', this.signupForm.value);
      // call login API
    
    this.service.register_user(this.signupForm.value).subscribe({
      next: (res)=>{
        if(res){
          console.log("✅ Success:", res);
        }
      },
       error: (err) => {
        console.error("❌ Error:", err);
      }
    })}
  }
  
}
