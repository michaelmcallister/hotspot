import { apiRequest } from './api';

export interface SearchResult {
  label: string;
  suburb: string;
  postcode: string;
  lga: string;
  risk_score: number;
}

export const searchService = {
  async search(query: string): Promise<SearchResult[]> {
    return apiRequest(`/search?q=${encodeURIComponent(query)}`);
  },
};