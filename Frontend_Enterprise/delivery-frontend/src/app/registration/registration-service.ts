import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";


@Injectable({
    providedIn:'root'
})

export class registration_service{
    private api_url='http://127.0.0.1:8000/core/register/';

    constructor(private http: HttpClient){

    }

    register_users(data:any):Observable<any>{
        return this.http.post(this.api_url,data)
    }

}