export interface Category {
  id: string;
  name: string;
}

export interface Article {
  id: number | string;
  title: string;
  content: string;
  category_id: number;
}
