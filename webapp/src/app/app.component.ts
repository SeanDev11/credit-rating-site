import { Component } from '@angular/core';
import { MY } from './ratings.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'webapp';

  currentCompanyMY;
  hasQueryOut;
  handleResult(company) {
    this.currentCompanyMY = company;
  }

  handleUserSearch(hasQuery) {
    this.hasQueryOut = hasQuery;
  }

}
