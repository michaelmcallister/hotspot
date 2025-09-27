import { apiRequest } from './api';

export interface ContactData {
  name: string;
  email: string;
  message: string;
  suburb?: string;
}

export interface ContactResponse {
  success: boolean;
  message: string;
}

export const contactService = {
  submitContact: async (data: ContactData): Promise<ContactResponse> => apiRequest('/contact', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};
