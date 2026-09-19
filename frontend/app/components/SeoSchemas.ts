export const BASE_URL = process.env.NEXT_PUBLIC_APP_URL || 'https://sih-ats-scanner.vercel.app';

export const organizationSchema = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'SIH ATS Scanner',
  url: BASE_URL,
  logo: `${BASE_URL}/logo.png`,
  description: 'Independent evaluation platform for Smart India Hackathon (SIH 2026) pitch presentations.',
};

export const softwareAppSchema = {
  '@context': 'https://schema.org',
  '@type': 'SoftwareApplication',
  name: 'SIH ATS Scanner',
  operatingSystem: 'All',
  applicationCategory: 'EducationalApplication',
  url: BASE_URL,
  description: 'SIH ATS Scanner evaluates Smart India Hackathon (SIH 2026) presentation decks against official 6-slide format guidelines, checking slide count, required sections, clarity, technical depth, and problem statement alignment.',
  offers: {
    '@type': 'Offer',
    price: '0',
    priceCurrency: 'INR',
  },
};

export const faqPageSchema = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'What does SIH ATS Scanner check in a Smart India Hackathon PPT?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'SIH ATS Scanner currently performs live automated screening for Structure & Format (6-slide ceiling limit, mandatory section headings), Presentation Clarity (word count density under 70 words per slide, visual diagram checks), and Problem Statement Alignment (semantic domain similarity). Technical Depth (AI checklist audit) and Originality (corpus comparison) require API key and dataset configuration, and are excluded with renormalized weights when unconfigured.',
      },
    },
    {
      '@type': 'Question',
      name: 'Is SIH ATS Scanner officially affiliated with Smart India Hackathon (SIH)?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'No. SIH ATS Scanner is an independent screening tool built for participants. It is not officially affiliated with, endorsed by, or sponsored by Smart India Hackathon (SIH), AICTE, or the Ministry of Education (MoE), Government of India.',
      },
    },
    {
      '@type': 'Question',
      name: 'What file formats are supported for evaluation?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'The scanner supports Microsoft PowerPoint (.pptx) and PDF (.pdf) documents up to 25MB in size.',
      },
    },
    {
      '@type': 'Question',
      name: 'How is technical depth evaluated?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'When an AI key is configured, Technical Depth is evaluated using a 4-point checklist checking for specific frameworks named, database technology specified, ML models, and workflow architecture. If unconfigured, Technical Depth is marked as unassessed and excluded from the total score without penalizing the deck.',
      },
    },
  ],
};
