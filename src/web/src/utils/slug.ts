import slugify from 'slugify';
import { searchService } from '../services';

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

export async function lookupSuburbBySlug(slug: string): Promise<any | null> {
  try {
    const parsed = parseSlug(slug);
    if (parsed) {
      const results = await searchService.search(parsed.suburb);

      if (results.length > 0) {
        const exactMatch = results.find((suburb: any) =>
          suburb.postcode === parsed.postcode
        );
        if (exactMatch) return exactMatch;

        return results[0];
      }
    }

    const searchTerm = slug.replace(/-/g, ' ');
    const results = await searchService.search(searchTerm);
    return results.length > 0 ? results[0] : null;
  } catch (error) {
    console.error('Error looking up suburb by slug:', error);
    return null;
  }
}
