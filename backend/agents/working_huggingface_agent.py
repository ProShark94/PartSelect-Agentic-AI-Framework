"""Working HuggingFace agent with a proven model."""

from __future__ import annotations
from typing import Optional
import torch
import json
import os


class WorkingHuggingFaceAgent:
    """HuggingFace agent using a proven conversational model."""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-small") -> None:
        """Initialize with a working conversational model.
        
        DialoGPT-small is proven to work and is:
        - Smaller (500MB vs 1GB+)
        - Faster inference
        - Better at conversations
        - Actually generates proper responses
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cpu")  # Keep simple for reliability
        
        # Load your training data for context
        self.training_data = self._load_training_data()
        
    def _load_training_data(self):
        """Load your training examples for better responses."""
        training_path = "data/training_conversations.json"
        if os.path.exists(training_path):
            try:
                with open(training_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
        
    def _load_model(self):
        """Load model on first use."""
        if self.model is None:
            try:
                from transformers import AutoModelForCausalLM, AutoTokenizer
                
                print(f"Loading proven model: {self.model_name}...")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float32,
                    low_cpu_mem_usage=True
                )
                
                # Fix tokenizer padding
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
                self.model.to(self.device)
                print("Model loaded successfully!")
                return True
            except Exception as e:
                print(f"Failed to load model: {e}")
                return False
        return True
    
    def _find_similar_training_example(self, query: str) -> Optional[str]:
        """Find similar training example to help with response."""
        query_lower = query.lower()
        best_match = None
        best_score = 0.0
        
        # Check for direct matches in training data
        for example in self.training_data:
            input_text = example.get('input', '').lower()
            
            # Calculate similarity score based on key words
            query_words = set(query_lower.split())
            input_words = set(input_text.split())
            
            # Remove common words
            common_words = {'the', 'a', 'an', 'is', 'are', 'my', 'i', 'to', 'from', 'in', 'on', 'at', 'with'}
            query_words = query_words - common_words
            input_words = input_words - common_words
            
            if not query_words or not input_words:
                continue
                
            # Calculate Jaccard similarity
            intersection = query_words.intersection(input_words)
            union = query_words.union(input_words)
            similarity = len(intersection) / len(union) if union else 0.0
            
            # Require at least 30% similarity and must be better than previous matches
            if similarity > 0.3 and similarity > best_score:
                best_score = similarity
                best_match = example.get('output', '')
        
        if best_match:
            print(f"DEBUG: Found training match with similarity: {best_score:.2f}")
            
        return best_match
        
    def call(self, prompt: str) -> Optional[str]:
        """Generate response using HuggingFace model with training context."""
        
        # First, check if we have a similar training example
        training_response = self._find_similar_training_example(prompt)
        if training_response:
            print(f"DEBUG: Using training data response")
            return training_response
        
        # Otherwise, use the model
        if not self._load_model():
            return None
            
        try:
            # Create a conversational prompt
            conversation_prompt = f"Customer: {prompt}\\nAssistant:"
            
            # Tokenize
            inputs = self.tokenizer.encode(
                conversation_prompt,
                return_tensors="pt",
                max_length=100,  # Keep short for DialoGPT-small
                truncation=True
            ).to(self.device)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=50,
                    min_new_tokens=10,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    early_stopping=True
                )
            
            # Decode
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract assistant response
            if "Assistant:" in full_response:
                response = full_response.split("Assistant:")[-1].strip()
                # Clean up
                response = response.replace("Customer:", "").strip()
                
                # Validate response quality
                if len(response) > 10 and "refrigerator" in response.lower() or "dishwasher" in response.lower() or "appliance" in response.lower() or "part" in response.lower():
                    return response
            
            return None
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if the agent can be used."""
        try:
            import transformers
            import torch
            return True
        except ImportError:
            return False
