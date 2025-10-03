import { apiRequest } from './api';

export interface Address {
  [key: string]: any;
}

export const addressService = {
  async getAddresses(postcode: string, query?: string): Promise<Address[]> {
    const url = query
      ? `/postcode/${postcode}/addresses?q=${encodeURIComponent(query)}`
      : `/postcode/${postcode}/addresses`;
    return apiRequest(url);
  },
};