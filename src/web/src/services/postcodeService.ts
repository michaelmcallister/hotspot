import { apiRequest } from './api';

export interface NearestSuburb {
  postcode: string;
  suburb: string;
  lga: string;
  distance_in_meters: number;
  parking_count?: number;
  risk_score?: number;
}

export interface TheftData {
  year: number;
  thefts: number;
}

export const postcodeService = {
  async getNearestSuburbs(postcode: string): Promise<NearestSuburb[]> {
    return apiRequest(`/postcode/${postcode}/nearest`);
  },

  async getTheftData(postcode: string): Promise<TheftData[]> {
    return apiRequest(`/postcode/${postcode}/thefts`);
  },
};