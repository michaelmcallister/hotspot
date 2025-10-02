import { apiRequest } from './api'

export interface FeedResponse {
  current: {
    postcode: string
    suburb: string
    risk_score: number
  }
  parking_submissions: Array<{
    parking_id: number
    address: string
    suburb: string
    postcode: string
    type: string
    lighting: number | null
    cctv: boolean | null
    created_at: string
    facilities: Array<{
      facility_id: number
      facility_name: string
    }>
  }>
  nearest_safer_suburbs: Array<{
    postcode: string
    suburb: string
    lga: string
    distance_in_meters: number
    risk_score: number
    parking_count: number
  }>
}

export const feedService = {
  async getPostcodeFeed(postcode: string): Promise<FeedResponse> {
    return apiRequest(`/postcode/${postcode}/feed`)
  }
}