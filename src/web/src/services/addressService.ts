import { apiRequest } from './api';

export interface Address {
  [key: string]: any;
}

export const addressService = {
  async getAddresses(postcode: string, query?: string): Promise<Address[]> {
    const url = query
      ? `/addresses/${postcode}?q=${encodeURIComponent(query)}`
      : `/addresses/${postcode}`;
    return apiRequest(url);
  },
};