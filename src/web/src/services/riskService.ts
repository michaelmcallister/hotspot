import { apiRequest } from './api';

export interface RiskData {
  [key: string]: any;
}

export interface TopRiskParams {
  scope?: string;
  page?: string;
  itemsPerPage?: string;
  sortBy?: string;
  sortOrder?: string;
  search?: string;
  [key: string]: string | undefined;
}

export interface TopRiskResponse {
  items: RiskData[];
  total: number;
}

export const riskService = {
  async getTopRisk(params: TopRiskParams = {}): Promise<TopRiskResponse> {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, value);
      }
    });
    return apiRequest(`/risk/top?${searchParams.toString()}`);
  },
};