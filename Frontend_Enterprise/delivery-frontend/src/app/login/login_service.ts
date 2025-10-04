import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";

@Injectable({
    providedIn:'root'
})

export class LoginService{
    private api_url='http://127.0.0.1:8000/core/login_user/'

    constructor(private http:HttpClient){}

    login(data:any):Observable<any>{
        return this.http.post(this.api_url,data)
    }
}