import { Routes } from '@angular/router';

import { ShellComponent } from './layout/shell.component';
import { QueryPage } from './pages/query/query.page';

export const routes: Routes = [
  {
    path: '',
    component: ShellComponent,
    children: [
      { path: '', redirectTo: 'query', pathMatch: 'full' },
      { path: 'query', component: QueryPage },
    ],
  },
  { path: '**', redirectTo: 'query' },
];
