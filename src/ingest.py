import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from src.schema import Principle6Schema

load_dotenv()

class IngestionEngine:
    """
    Handles the loading of PDF documents, text chunking, and 
    structured extraction of Principle 6 data.
    """
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name
        self.chunk_size = 2000
        self.chunk_overlap = 200
        self._extractor = None

    @property
    def extractor(self):
        if self._extractor is None:
            # Initialize LLM with structured output capability only when needed
            try:
                llm = ChatOpenAI(model=self.model_name, temperature=0)
                self._extractor = llm.with_structured_output(Principle6Schema)
            except Exception as e:
                print(f"⚠️ Warning: LLM Init failed (Check API Key): {e}")
                return None
        return self._extractor

    def load_and_chunk(self, pdf_path: str) -> List[dict]:
        """
        Loads a PDF and splits it into chunks with metadata (Page numbers).
        CalQuity-style: Preserves page numbers for citation.
        """
        print(f"📄 Loading PDF: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        
        chunks = splitter.split_documents(pages)
        print(f"✅ Created {len(chunks)} chunks from {len(pages)} pages.")
        
        # Convert to list of dicts for easier handling/serialization later
        return [{"text": c.page_content, "metadata": c.metadata} for c in chunks]

    def extract_principle_6(self, text_context: str) -> Principle6Schema:
        """
        DataWeave-style: Uses an LLM Agent to parse the text into the strictly defined Pydantic Schema.
        """
        system_prompt = """
        You are an Expert ESG Auditor. Your task is to extract specifics for 'Principle 6' (Environmental Responsibilities) 
        from the provided Corporate BRSR Report text.
        
        Focus on:
        1. Scope 1, 2, 3 Emissions.
        2. Waste Management details.
        3. Water Consumption metrics.
        
        Rules:
        - If a value is explicit, extract it.
        - If a value is NOT present, leave it as null (do NOT guess or hallucinate).
        - Convert units to the standard requested in the schema if possible, or note the discrepancy.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Analyze the following text and extract Principle 6 data:\n\n{text}")
        ])
        
        chain = prompt | self.extractor
        
        print("🤖 Running Extraction Agent...")
        try:
            result = chain.invoke({"text": text_context})
            return result
        except Exception as e:
            print(f"❌ Extraction Failed: {e}")
            return Principle6Schema() # Return empty schema on fail

if __name__ == "__main__":
    # Test run
    engine = IngestionEngine()
    # Note: efficient testing would typically just load a few pages or a specific section
    print("Ingestion Engine initialized.")
