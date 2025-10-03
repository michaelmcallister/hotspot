import { apiRequest } from './api';

export interface RiskData {
  [key: string]: any;
}

export interface TopRiskParams {
  scope?: string;
  order?: string;
  limit?: string;
  [key: string]: string | undefined;
}

export const riskService = {
  async getTopRisk(params: TopRiskParams = {}): Promise<RiskData[]> {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, value);
      }
    });
    return apiRequest(`/risk/top?${searchParams.toString()}`);
  },

  async compareRisk(postcode: string): Promise<RiskData> {
    return apiRequest(`/risk/compare?postcode=${postcode}`);
  },
};