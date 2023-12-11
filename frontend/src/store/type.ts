export interface Category {
  id: number;
  name: string;
}

export interface Article {
  id: number;
  title: string;
  content: string;
  category_id: number; // Adjust according to your actual data structure
}
