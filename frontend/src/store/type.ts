export interface Category {
  id: string;
  name: string;
}

export interface Article {
  id: number | string;
  title: string;
  content: string;
  category_id: number;
  comments: Comment[];
  showComments: boolean
}

export interface Comment {
  id: number;
  content: string;
  userId: number;
  articleId: number;
  createdAt: {
    toString: () => string;
    toDateString: () => string;
  };
  editing?: boolean; // Define the 'editing' property as optional
  updatedContent?: string; // Define the 'updatedContent' property as optional
}