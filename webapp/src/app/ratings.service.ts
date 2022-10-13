import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';

export interface MY {
  _id: string,
  company: string,
  ticker: string,
  industry: string,
  ratings: Array<Object>
}

export interface SAP {
  _id: string,
  company: string,
  ticker: string,
  industry: string,
  ratings: Array<Object>
}

export interface CombinedRatings {
  _id?: string,
  company?: string,
  ticker?: string,
  industry?: string,
  ratingsMY: Array<Object>,
  ratingsSAP: Array<Object>
}

@Injectable({
  providedIn: 'root'
})

export class RatingsService {

  constructor(private http:HttpClient) { }

  searchCompanies(query: string) {
    
    return this.http.post<{payload: Array<CombinedRatings>}>('/api/getCompanies', {payload: query}, {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    }).pipe(
      map(data => data.payload)
    );
  }

  searchMoodys(query: string) {
    return this.http.post<{payload: Array<MY>}>('/api/getCompanies', {payload: query}, {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    }).pipe(
      map(data => data.payload)
    );
  }

  searchSP(query: string) {
    return
  }
}