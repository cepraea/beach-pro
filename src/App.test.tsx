import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it } from 'vitest';
import App from './App';

describe('App', () => {
  it('identifica o produto na tela inicial', () => {
    expect(renderToStaticMarkup(<App />)).toContain('CEPRAEA Beach Pro');
  });
});
