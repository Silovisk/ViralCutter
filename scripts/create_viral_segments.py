import json
import re
import random

def create(num_segments, viral_mode, themes, tempo_minimo, tempo_maximo):
    """
    Create viral segments from video transcript using rule-based analysis.
    Returns a structured JSON with viral segments.
    """
    try:
        with open('tmp/input_video.tsv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: input_video.tsv not found in tmp/ directory")
        return None
    
    # Parse TSV file
    segments = []
    for line in lines[1:]:  # Skip header
        if line.strip():
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                start_time = float(parts[0])
                end_time = float(parts[1])
                text = parts[2]
                segments.append({
                    'start': start_time,
                    'end': end_time,
                    'text': text,
                    'duration': end_time - start_time
                })
    
    if not segments:
        print("No transcript segments found")
        return None
    
    print(f"Analyzing {len(segments)} transcript segments...")
    
    # Define viral indicators (keywords that suggest viral content)
    viral_keywords = [
        # Emotional reactions
        'incrível', 'surpreendente', 'chocante', 'louco', 'insano', 'cara', 'mano',
        'nossa', 'uau', 'impressionante', 'bizarro', 'esquisito', 'estranho',
        # Trending topics
        'ai', 'inteligência artificial', 'chatgpt', 'openai', 'tecnologia',
        'bitcoin', 'crypto', 'nft', 'metaverso', 'tiktok', 'youtube',
        # Questions and engagement
        'como', 'porque', 'será', 'imagine', 'vocês sabiam', 'você sabia',
        'acredita', 'pensa', 'acha', 'imagina',
        # Dramatic expressions
        'nunca', 'sempre', 'jamais', 'impossível', 'inacreditável',
        'segredo', 'revelação', 'verdade', 'mentira'
    ]
    
    # Score segments based on viral potential
    scored_segments = []
    for i, segment in enumerate(segments):
        score = 0
        text_lower = segment['text'].lower()
        
        # Check for viral keywords
        for keyword in viral_keywords:
            if keyword in text_lower:
                score += 10
        
        # Boost score for segments with questions
        if '?' in segment['text']:
            score += 15
        
        # Boost score for segments with exclamations
        exclamation_count = segment['text'].count('!')
        score += exclamation_count * 5
        
        # Boost score for segments with emotional words
        emotional_words = ['cara', 'mano', 'nossa', 'uau', 'incrível']
        for word in emotional_words:
            score += text_lower.count(word) * 8
        
        # Penalty for very short segments
        if segment['duration'] < 3:
            score -= 20
        
        # Boost for optimal duration segments
        if 10 <= segment['duration'] <= 30:
            score += 10
        
        scored_segments.append({
            'index': i,
            'start': segment['start'],
            'end': segment['end'],
            'text': segment['text'],
            'duration': segment['duration'],
            'score': max(0, score)  # Ensure score is not negative
        })
    
    # Sort by score (highest first)
    scored_segments.sort(key=lambda x: x['score'], reverse=True)
    
    # Create viral segments by combining consecutive high-scoring segments
    viral_segments = []
    used_indices = set()
    
    for target_segment in scored_segments[:num_segments * 3]:  # Consider top candidates
        if target_segment['index'] in used_indices:
            continue
            
        # Try to create a segment that meets duration requirements
        start_idx = target_segment['index']
        end_idx = start_idx
        current_duration = target_segment['duration']
        
        # Extend forward to meet minimum duration
        while current_duration < tempo_minimo and end_idx < len(segments) - 1:
            end_idx += 1
            if end_idx < len(segments):
                current_duration = segments[end_idx]['end'] - segments[start_idx]['start']
        
        # Extend backward if needed
        while current_duration < tempo_minimo and start_idx > 0:
            start_idx -= 1
            current_duration = segments[end_idx]['end'] - segments[start_idx]['start']
        
        # Trim if too long
        while current_duration > tempo_maximo and end_idx > start_idx:
            end_idx -= 1
            current_duration = segments[end_idx]['end'] - segments[start_idx]['start']
        
        # Check if duration is within bounds
        if tempo_minimo <= current_duration <= tempo_maximo:
            # Mark indices as used
            for idx in range(start_idx, end_idx + 1):
                used_indices.add(idx)
            
            # Combine text from all segments in range
            combined_text = ' '.join([segments[idx]['text'] for idx in range(start_idx, end_idx + 1)])
            
            # Calculate average score for the range
            avg_score = sum([scored_segments[idx]['score'] for idx in range(start_idx, end_idx + 1) 
                           if idx < len(scored_segments)]) // (end_idx - start_idx + 1)
            
            viral_segments.append({
                'start_time': seconds_to_timestamp(segments[start_idx]['start']),
                'end_time': seconds_to_timestamp(segments[end_idx]['end']),
                'duration': int(current_duration),
                'text': combined_text,
                'score': min(100, max(30, avg_score + random.randint(10, 30)))  # Ensure score is between 30-100
            })
            
            if len(viral_segments) >= num_segments:
                break
    
    # If we don't have enough segments, create some from remaining high-scoring content
    while len(viral_segments) < num_segments and len(scored_segments) > 0:
        # Find unused segments
        unused_segments = [s for s in scored_segments if s['index'] not in used_indices]
        if not unused_segments:
            break
            
        segment = unused_segments[0]
        used_indices.add(segment['index'])
        
        viral_segments.append({
            'start_time': seconds_to_timestamp(segment['start']),
            'end_time': seconds_to_timestamp(segment['end']),
            'duration': int(segment['duration']),
            'text': segment['text'],
            'score': min(100, max(20, segment['score'] + random.randint(5, 25)))
        })
    
    # Generate titles and descriptions
    for i, segment in enumerate(viral_segments):
        # Generate a simple title based on content
        text_words = segment['text'].split()[:5]  # First 5 words
        title = ' '.join(text_words)
        if len(title) > 50:
            title = title[:47] + "..."
        
        segment['title'] = title.capitalize()
        segment['description'] = segment['text'][:100] + "..." if len(segment['text']) > 100 else segment['text']
    
    # Prepare final JSON structure
    result = {
        "segments": [
            {
                "title": segment['title'],
                "start_time": segment['start_time'],
                "end_time": segment['end_time'],
                "description": segment['description'],
                "duration": segment['duration'],
                "score": segment['score']
            }
            for segment in viral_segments
        ]
    }
    
    print(f"Created {len(viral_segments)} viral segments:")
    for i, segment in enumerate(viral_segments):
        print(f"  Segment {i+1}: {segment['start_time']} - {segment['end_time']} ({segment['duration']}s) - Score: {segment['score']}")
    
    return result

def seconds_to_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"