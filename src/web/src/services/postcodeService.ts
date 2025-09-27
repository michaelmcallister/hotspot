import { apiRequest } from './api';

export interface NearestSuburb {
  postcode: string;
  suburb: string;
  lga: string;
  distance_in_meters: number;
  parking_count?: number;
  risk_score?: number;
}

export const postcodeService = {
  getNearestSuburbs: async (postcode: string): Promise<NearestSuburb[]> => apiRequest(`/postcode/${postcode}/nearest`),
};
