export const REPORTS = {
  sales: {
    title: 'Sales by region',
    columns: ['Region', 'Quarter', 'Revenue'],
    rows: [
      ['North', 'Q1', 120000],
      ['North', 'Q2', 134000],
      ['South', 'Q1', 98000],
      ['South', 'Q2', 101500],
      ['West', 'Q1', 143200],
      ['West', 'Q2', 150900],
    ],
  },
  headcount: {
    title: 'Headcount by team',
    columns: ['Team', 'Quarter', 'People'],
    rows: [
      ['Platform', 'Q1', 14],
      ['Platform', 'Q2', 16],
      ['Product', 'Q1', 22],
      ['Product', 'Q2', 25],
    ],
  },
};

export const COMPANY = { name: 'PlusPort by Visma', city: 'Zoetermeer' };
