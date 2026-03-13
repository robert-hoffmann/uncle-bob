import { describe, it, expect } from 'vitest';

describe('token validation', () => {
  it('returns unauthorized error for missing token boundary', () => {
    const result = validateToken('');
    expect(result.ok).toEqual(false);
  });
});
