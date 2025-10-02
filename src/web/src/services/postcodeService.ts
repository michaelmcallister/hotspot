import { apiRequest } from './api';

export interface TheftData {
  year: number;
  thefts: number;
}

export const postcodeService = {
  async getTheftData(postcode: string): Promise<TheftData[]> {
    return apiRequest(`/postcode/${postcode}/thefts`);
  },
};