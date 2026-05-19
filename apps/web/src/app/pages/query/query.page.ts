import { Component } from '@angular/core';

@Component({
  selector: 'app-query-page',
  template: `
    <section>
      <h1>Query</h1>
      <p>Submit campus questions against the retrieval and orchestration pipeline.</p>
      <p class="placeholder">Query submission is not wired in phase 0.</p>
    </section>
  `,
  styles: [
    `
      h1 {
        margin: 0 0 0.5rem;
        font-size: 1.25rem;
        font-weight: 600;
      }
      p {
        margin: 0 0 0.75rem;
        color: #444;
      }
      .placeholder {
        font-size: 0.875rem;
        color: #666;
      }
    `,
  ],
})
export class QueryPage {}
