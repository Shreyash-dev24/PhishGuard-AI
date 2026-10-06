const API_BASE_URL = "";


export interface PredictionResponse {
  url: string;
  classification: "legitimate" | "potentially_phishing";
  final_score: number;
  ml_probability_phishing: number;
  dl_probability_phishing: number;
  raw_score: number;
  indicator_count: number;
  indicator_boost: number;
  triggered_indicators: string[];
}


export interface PredictionHistoryResponse
  extends PredictionResponse {
  id: number;
  created_at: string;
}


export async function predictUrl(
  url: string
): Promise<PredictionResponse> {

  const response = await fetch(
    `${API_BASE_URL}/api/predict`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        url,
      }),
    }
  );


  if (!response.ok) {

    const errorData =
      await response.json().catch(() => null);

    throw new Error(
      errorData?.detail ||
      "Prediction request failed."
    );
  }


  return response.json();
}


export async function getPredictionHistory(): Promise<
  PredictionHistoryResponse[]
> {

  const response = await fetch(
    `${API_BASE_URL}/api/history`
  );


  if (!response.ok) {

    const errorData =
      await response.json().catch(() => null);

    throw new Error(
      errorData?.detail ||
      "Failed to load prediction history."
    );
  }


  return response.json();
}