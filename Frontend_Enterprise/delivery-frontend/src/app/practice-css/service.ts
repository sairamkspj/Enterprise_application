import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { HttpClient } from "@angular/common/http";


@Injectable({
    providedIn:'root'
})

export class login_reg_Service{
    private url='http://127.0.0.1:8000/core/';

    constructor(private http:HttpClient){

    }

    register_user(data:any):Observable<any>{
        return this.http.post(this.url+'register/',data);
    }
}