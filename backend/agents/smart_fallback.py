"""Enhanced fallback system using your training data."""

import json
import os
from typing import Optional, Dict, Any


class SmartFallbackSystem:
    """Intelligent fallback that uses your training data for relevant responses."""
    
    def __init__(self):
        self.training_data = self._load_training_data()
        print(f"Loaded {len(self.training_data)} training examples for smart fallback")
    
    def _load_training_data(self):
        """Load your training examples."""
        training_path = "data/training_conversations.json"
        if os.path.exists(training_path):
            try:
                with open(training_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _calculate_similarity(self, query: str, training_input: str) -> float:
        """Calculate similarity between query and training example."""
        query_words = set(query.lower().split())
        training_words = set(training_input.lower().split())
        
        if not query_words or not training_words:
            return 0.0
            
        # Calculate Jaccard similarity
        intersection = query_words.intersection(training_words)
        union = query_words.union(training_words)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _find_best_training_match(self, query: str) -> Optional[Dict[str, Any]]:
        """Find the best matching training example."""
        if not self.training_data:
            return None
            
        best_match = None
        best_score = 0.0
        
        for example in self.training_data:
            similarity = self._calculate_similarity(query, example.get('input', ''))
            
            # Boost similarity for key appliance terms
            query_lower = query.lower()
            input_lower = example.get('input', '').lower()
            appliance_terms = {'refrigerator', 'fridge', 'dishwasher', 'washing', 'machine', 'dryer', 
                             'cooling', 'cleaning', 'leaking', 'filter', 'light', 'bulb', 'water'}
            
            appliance_boost = 0
            for term in appliance_terms:
                if term in query_lower and term in input_lower:
                    appliance_boost += 0.15
                    
            final_similarity = similarity + appliance_boost
            
            # Lower threshold to 20% and include appliance boost
            if final_similarity > 0.2 and final_similarity > best_score:
                best_score = final_similarity
                best_match = example
                
        return best_match
    
    def get_smart_response(self, query: str) -> str:
        """Get intelligent response using training data + enhanced fallback."""
        
        # First, try to find a relevant training example
        best_match = self._find_best_training_match(query)
        if best_match:
            print(f"DEBUG: Using training data match (similarity: {self._calculate_similarity(query, best_match.get('input', '')):.2f})")
            return best_match.get('output', '')
        
        # If no good match, use enhanced keyword-based responses
        query_lower = query.lower()
        
        # Refrigerator issues
        if any(word in query_lower for word in ['refrigerator', 'fridge', 'cooling', 'cold', 'temperature']):
            if 'not cooling' in query_lower or 'warm' in query_lower:
                return "For refrigerator cooling issues, check: 1) Temperature settings (should be 37-40°F), 2) Clean condenser coils (usually on back or bottom), 3) Door seals for gaps, 4) Frost buildup in freezer. If these don't help, you may need a new thermostat, evaporator fan, or compressor."
            elif 'leaking' in query_lower or 'water' in query_lower:
                return "Refrigerator water leaks usually come from: 1) Clogged defrost drain, 2) Loose water supply line, 3) Cracked drain pan, 4) Bad water filter. Check these components and replace as needed."
            elif 'light' in query_lower or 'bulb' in query_lower:
                return "Refrigerator lights use special appliance bulbs rated for cold temperatures. You'll need your refrigerator's model number to find the correct replacement bulb. Check inside the fridge or on the door frame for the model number."
            else:
                return "I can help with refrigerator parts! Common issues include cooling problems, water leaks, faulty lights, and ice maker issues. Please describe your specific problem and provide your model number for accurate part recommendations."
        
        # Water filter queries
        elif any(word in query_lower for word in ['water filter', 'filter']):
            return "To find the right water filter: 1) Locate your refrigerator's model number (inside the fridge or on door frame), 2) Remove the old filter and check for part numbers, 3) Search for compatible filters using the model number. Most filters need replacement every 6 months."
        
        # Dishwasher issues
        elif any(word in query_lower for word in ['dishwasher', 'dishes', 'washing']):
            if 'not cleaning' in query_lower or 'dirty' in query_lower:
                return "For dishwasher cleaning issues: 1) Clean the filter (bottom of dishwasher), 2) Check spray arms for clogs, 3) Use proper detergent amount, 4) Don't overcrowd dishes. You may need new spray arms or wash pump motor."
            elif 'not draining' in query_lower or 'water' in query_lower:
                return "Dishwasher drainage problems usually require: 1) Clean the drain filter, 2) Check garbage disposal connection, 3) Clear drain hose clogs, 4) Replace drain pump if needed."
            else:
                return "I can help with dishwasher parts! Common issues include poor cleaning, drainage problems, door seal leaks, and control panel failures. What specific problem are you experiencing?"
        
        # Installation help
        elif any(word in query_lower for word in ['install', 'replace', 'how to', 'installation']):
            return "For installation help, I need to know: 1) What part you're installing, 2) Your appliance model number, 3) What tools you have available. Most parts come with instructions, but I can provide specific guidance once I know the details."
        
        # Compatibility questions
        elif any(word in query_lower for word in ['compatible', 'fit', 'work with']):
            return "To check part compatibility, I need: 1) The exact part number, 2) Your appliance's complete model number. You can find the model number on a sticker inside your appliance or on the back/side panel."
        
        # General help
        elif any(word in query_lower for word in ['help', 'hello', 'hi']):
            return "Hello! I specialize in appliance parts for dishwashers and refrigerators. I can help you find parts, check compatibility, and provide installation guidance. What appliance are you working on today?"
        
        # Default response
        else:
            return "I'm here to help with appliance parts and repairs! I can assist with dishwashers and refrigerators. Please tell me: 1) What type of appliance, 2) What problem you're experiencing, 3) Your model number if you have it."
