import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-shell',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="shell">
      <header class="shell-header">
        <span class="brand">CampusIQ</span>
        <nav>
          <a routerLink="/query" routerLinkActive="active">Query</a>
        </nav>
      </header>
      <main class="shell-main">
        <router-outlet />
      </main>
    </div>
  `,
  styles: [
    `
      .shell {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        font-family: system-ui, sans-serif;
      }
      .shell-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #e5e5e5;
      }
      .brand {
        font-weight: 600;
        letter-spacing: 0.02em;
      }
      nav a {
        color: #333;
        text-decoration: none;
        margin-left: 1rem;
      }
      nav a.active {
        text-decoration: underline;
      }
      .shell-main {
        flex: 1;
        padding: 1.5rem;
        max-width: 48rem;
      }
    `,
  ],
})
export class ShellComponent {}
