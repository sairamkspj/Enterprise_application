import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { registration_service } from './registration-service';
import { RouterModule } from '@angular/router';


@Component({
  selector: 'app-registration',
  standalone:true,
  imports: [FormsModule,CommonModule,RouterModule],
  templateUrl: './registration.html',
  styleUrls: ['./registration.css']
})
export class Registration {

  Name='';
  Email='';
  Password='';
  Role = '';
  previewData: any = null;
  Restaurent_name='';
  Contact_number='';
  Location='';
  User_reg_sucess:boolean=false;

  constructor (private regservice:registration_service){}
  onSubmit(){

    const data={
      username: this.Name,
      email: this.Email,
      role: this.Role,
      password: this.Password,
      Restaurent_name: this.Restaurent_name,
      Contact_number:this.Contact_number,
      Location:this.Location,
    }

    this.regservice.register_users(data).subscribe({
      next: (res) => {
        if(res){
        console.log("✅ Success:", res);
        this.previewData = res.saved_user; 
        this.User_reg_sucess=true;
        }
      },
      error: (err) => {
        console.error("❌ Error:", err);
      }
    });

  }

}
