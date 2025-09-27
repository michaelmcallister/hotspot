import { apiRequest } from './api';

export interface SearchResult {
  label: string;
  suburb: string;
  postcode: string;
  lga: string;
  risk_score: number;
}

export const searchService = {
  search: async (query: string): Promise<SearchResult[]> => apiRequest(`/search?q=${encodeURIComponent(query)}`),
};
