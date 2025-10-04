import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class logfile_Service {
  private url = 'http://127.0.0.1:8000/logfile/';

  constructor(private http: HttpClient) {}

  Send_data(data: any): Observable<any> {
    return this.http.post(this.url + 'upload/', data);
  }

  processLogs(source: string): Observable<any> {
    const data=this.http.get(`${this.url}process-logs/?source=${source}`)
    console.log('new data'+data)
    return this.http.get(`${this.url}process-logs/?source=${source}`);
  }

  getTaskStatus(taskId: string): Observable<any> {
    return this.http.get(`${this.url}task-status/${taskId}/`);
  }
}
