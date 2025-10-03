import slugify from 'slugify';

export function createSlug(suburb: string, postcode: string): string {
  return slugify(`${suburb} ${postcode}`, { lower: true, strict: true });
}

export function parseSlug(slug: string): { suburb: string; postcode: string } | null {
  const parts = slug.split('-');
  if (parts.length < 2) return null;

  const postcode = parts[parts.length - 1];
  const suburb = parts.slice(0, -1).join(' ');

  return { suburb, postcode };
}