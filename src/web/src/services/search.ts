export type SearchResult = { label: string; suburb?: string; postcode?: string; state?: string };

const MOCK: SearchResult[] = [
  { label: "Melbourne, 3000 (VIC)", suburb: "Melbourne", postcode: "3000", state: "VIC" },
  { label: "Carlton, 3053 (VIC)", suburb: "Carlton", postcode: "3053", state: "VIC" },
  { label: "Fitzroy, 3065 (VIC)", suburb: "Fitzroy", postcode: "3065", state: "VIC" },
  { label: "Brunswick, 3056 (VIC)", suburb: "Brunswick", postcode: "3056", state: "VIC" },
];

export async function fetchSearchResults(q: string): Promise<SearchResult[]> {
  if (!q) return [];
  // TODO: replace with API call when done, format might change!
  const s = q.toLowerCase();
  return MOCK.filter(x => x.label.toLowerCase().includes(s)).slice(0, 8);
}
