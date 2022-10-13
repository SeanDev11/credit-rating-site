import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

import { CombinedRatings } from './ratings.service';


@Injectable({
  providedIn: 'root'
})
export class SearchBarServiceService {
  private _currentCompany: BehaviorSubject<CombinedRatings> = new BehaviorSubject<CombinedRatings>({
    company: 'null',  
    ratingsMY: [],
    ratingsSAP: []
  });
  

  public readonly currentCompany: Observable<CombinedRatings> = this._currentCompany.asObservable();

  private _hasQuery: BehaviorSubject<Boolean> = new BehaviorSubject<Boolean>(false);
  public readonly hasQuery: Observable<Boolean> = this._hasQuery.asObservable();
  /*get currentCompany$() {
    return this.currentCompany.asObservable();
  }
  
  setCurrentCompany(company: CombinedRatings) {
    this.currentCompany$.next(company);
  }*/

  setCurrentCompany(company: CombinedRatings) {
    return this._currentCompany.next(company);
  }

  setHasQuery(bool: Boolean) {
    return this._hasQuery.next(bool);
  }
  /*get currentCompany() {
    return Observable(this._currentCompany);
  }*/

  constructor() { }
}
