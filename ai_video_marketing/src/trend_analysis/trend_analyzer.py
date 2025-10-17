"""
Trend Analyzer - Tìm kiếm và phân tích xu hướng video
"""
import requests
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
import pandas as pd
from dataclasses import dataclass
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VideoData:
    """Data class for video information"""
    title: str
    description: str
    views: int
    likes: int
    comments: int
    duration: int
    upload_date: str
    url: str
    thumbnail: str
    tags: List[str]
    platform: str

class TrendAnalyzer:
    """Phân tích xu hướng video từ các platform"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def search_trending_keywords(self, 
                               keywords: List[str],
                               max_results: int = 50) -> List[VideoData]:
        """
        Tìm kiếm video theo từ khóa trending
        
        Args:
            keywords: Danh sách từ khóa
            max_results: Số lượng video tối đa
            
        Returns:
            List[VideoData]: Danh sách video trending
        """
        all_videos = []
        
        for keyword in keywords:
            logger.info(f"Searching for keyword: {keyword}")
            
            # Search on different platforms
            youtube_videos = self._search_youtube(keyword, max_results // len(keywords))
            tiktok_videos = self._search_tiktok(keyword, max_results // len(keywords))
            
            all_videos.extend(youtube_videos)
            all_videos.extend(tiktok_videos)
            
            # Rate limiting
            time.sleep(1)
        
        # Sort by engagement score
        all_videos.sort(key=lambda x: self._calculate_engagement_score(x), reverse=True)
        
        return all_videos[:max_results]
    
    def _search_youtube(self, keyword: str, max_results: int) -> List[VideoData]:
        """Tìm kiếm video trên YouTube"""
        videos = []
        
        try:
            # YouTube Data API v3 search
            api_key = self.config.get("youtube_api_key")
            if not api_key:
                logger.warning("YouTube API key not found, using mock data")
                return self._get_mock_youtube_data(keyword, max_results)
            
            # Search parameters
            search_url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': keyword,
                'type': 'video',
                'order': 'relevance',
                'maxResults': max_results,
                'publishedAfter': (datetime.now() - timedelta(days=7)).isoformat() + 'Z',
                'key': api_key
            }
            
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Get video details
            video_ids = [item['id']['videoId'] for item in data['items']]
            video_details = self._get_youtube_video_details(video_ids, api_key)
            
            for item, details in zip(data['items'], video_details):
                video = VideoData(
                    title=item['snippet']['title'],
                    description=item['snippet']['description'],
                    views=details.get('viewCount', 0),
                    likes=details.get('likeCount', 0),
                    comments=details.get('commentCount', 0),
                    duration=self._parse_duration(details.get('duration', 'PT0S')),
                    upload_date=item['snippet']['publishedAt'],
                    url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    thumbnail=item['snippet']['thumbnails']['high']['url'],
                    tags=item['snippet'].get('tags', []),
                    platform='youtube'
                )
                videos.append(video)
                
        except Exception as e:
            logger.error(f"Error searching YouTube: {e}")
            # Return mock data as fallback
            videos = self._get_mock_youtube_data(keyword, max_results)
        
        return videos
    
    def _search_tiktok(self, keyword: str, max_results: int) -> List[VideoData]:
        """Tìm kiếm video trên TikTok"""
        videos = []
        
        try:
            # TikTok API (if available) or web scraping
            # For now, return mock data
            videos = self._get_mock_tiktok_data(keyword, max_results)
            
        except Exception as e:
            logger.error(f"Error searching TikTok: {e}")
            videos = self._get_mock_tiktok_data(keyword, max_results)
        
        return videos
    
    def _get_youtube_video_details(self, video_ids: List[str], api_key: str) -> List[Dict]:
        """Lấy chi tiết video YouTube"""
        try:
            details_url = "https://www.googleapis.com/youtube/v3/videos"
            params = {
                'part': 'statistics,contentDetails',
                'id': ','.join(video_ids),
                'key': api_key
            }
            
            response = self.session.get(details_url, params=params)
            response.raise_for_status()
            
            return response.json()['items']
            
        except Exception as e:
            logger.error(f"Error getting YouTube video details: {e}")
            return [{} for _ in video_ids]
    
    def _parse_duration(self, duration: str) -> int:
        """Parse ISO 8601 duration to seconds"""
        import re
        
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration)
        
        if not match:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    def _calculate_engagement_score(self, video: VideoData) -> float:
        """Tính điểm tương tác của video"""
        if video.views == 0:
            return 0
        
        # Engagement rate = (likes + comments) / views
        engagement_rate = (video.likes + video.comments) / video.views
        
        # Weight by recency (newer videos get higher score)
        upload_date = datetime.fromisoformat(video.upload_date.replace('Z', '+00:00'))
        days_old = (datetime.now(upload_date.tzinfo) - upload_date).days
        recency_factor = max(0.1, 1 - (days_old / 30))  # Decay over 30 days
        
        return engagement_rate * recency_factor * video.views
    
    def _get_mock_youtube_data(self, keyword: str, max_results: int) -> List[VideoData]:
        """Mock data for YouTube (when API is not available)"""
        mock_videos = []
        
        for i in range(max_results):
            video = VideoData(
                title=f"Trending {keyword} Video {i+1}",
                description=f"Amazing content about {keyword} that's going viral!",
                views=10000 + i * 5000,
                likes=500 + i * 200,
                comments=50 + i * 20,
                duration=60 + i * 30,
                upload_date=(datetime.now() - timedelta(days=i)).isoformat(),
                url=f"https://youtube.com/watch?v=mock{i}",
                thumbnail=f"https://img.youtube.com/vi/mock{i}/maxresdefault.jpg",
                tags=[keyword, "trending", "viral"],
                platform="youtube"
            )
            mock_videos.append(video)
        
        return mock_videos
    
    def _get_mock_tiktok_data(self, keyword: str, max_results: int) -> List[VideoData]:
        """Mock data for TikTok"""
        mock_videos = []
        
        for i in range(max_results):
            video = VideoData(
                title=f"#{keyword} trending on TikTok {i+1}",
                description=f"Viral TikTok about {keyword}",
                views=50000 + i * 10000,
                likes=2000 + i * 500,
                comments=100 + i * 50,
                duration=15 + i * 5,
                upload_date=(datetime.now() - timedelta(days=i)).isoformat(),
                url=f"https://tiktok.com/@user/video/{i}",
                thumbnail=f"https://p16-sign.tiktokcdn-us.com/mock{i}.jpeg",
                tags=[keyword, "tiktok", "viral", "fyp"],
                platform="tiktok"
            )
            mock_videos.append(video)
        
        return mock_videos
    
    def analyze_trending_patterns(self, videos: List[VideoData]) -> Dict[str, Any]:
        """
        Phân tích patterns trong video trending
        
        Args:
            videos: Danh sách video
            
        Returns:
            Dict[str, Any]: Kết quả phân tích
        """
        if not videos:
            return {}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame([{
            'title': v.title,
            'views': v.views,
            'likes': v.likes,
            'comments': v.comments,
            'duration': v.duration,
            'platform': v.platform,
            'tags': v.tags
        } for v in videos])
        
        analysis = {
            'total_videos': len(videos),
            'platform_distribution': df['platform'].value_counts().to_dict(),
            'avg_views': df['views'].mean(),
            'avg_likes': df['likes'].mean(),
            'avg_comments': df['comments'].mean(),
            'avg_duration': df['duration'].mean(),
            'top_performing_videos': df.nlargest(5, 'views')[['title', 'views', 'likes']].to_dict('records'),
            'common_tags': self._extract_common_tags(videos),
            'duration_analysis': self._analyze_duration_patterns(df),
            'engagement_analysis': self._analyze_engagement_patterns(df)
        }
        
        return analysis
    
    def _extract_common_tags(self, videos: List[VideoData]) -> Dict[str, int]:
        """Trích xuất tags phổ biến"""
        tag_counts = {}
        
        for video in videos:
            for tag in video.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Sort by frequency
        return dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20])
    
    def _analyze_duration_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Phân tích patterns về thời lượng video"""
        return {
            'short_videos': len(df[df['duration'] <= 30]),
            'medium_videos': len(df[(df['duration'] > 30) & (df['duration'] <= 120)]),
            'long_videos': len(df[df['duration'] > 120]),
            'optimal_duration': df.groupby(pd.cut(df['duration'], bins=5))['views'].mean().idxmax()
        }
    
    def _analyze_engagement_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Phân tích patterns về tương tác"""
        df['engagement_rate'] = (df['likes'] + df['comments']) / df['views']
        
        return {
            'avg_engagement_rate': df['engagement_rate'].mean(),
            'high_engagement_videos': len(df[df['engagement_rate'] > 0.05]),
            'platform_engagement': df.groupby('platform')['engagement_rate'].mean().to_dict()
        }
    
    def save_analysis(self, 
                     videos: List[VideoData], 
                     analysis: Dict[str, Any],
                     output_dir: Path) -> Path:
        """
        Lưu kết quả phân tích
        
        Args:
            videos: Danh sách video
            analysis: Kết quả phân tích
            output_dir: Thư mục lưu
            
        Returns:
            Path: Đường dẫn file đã lưu
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save videos data
        videos_data = []
        for video in videos:
            videos_data.append({
                'title': video.title,
                'description': video.description,
                'views': video.views,
                'likes': video.likes,
                'comments': video.comments,
                'duration': video.duration,
                'upload_date': video.upload_date,
                'url': video.url,
                'thumbnail': video.thumbnail,
                'tags': video.tags,
                'platform': video.platform
            })
        
        # Save to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"trend_analysis_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'videos': videos_data,
                'analysis': analysis,
                'generated_at': datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Analysis saved to: {output_file}")
        return output_file

# Example usage
if __name__ == "__main__":
    from configs.config import TREND_CONFIG, OUTPUTS_DIR
    
    # Initialize analyzer
    analyzer = TrendAnalyzer(TREND_CONFIG)
    
    # Search trending keywords
    keywords = ["cooking", "fashion", "tech review", "travel", "fitness"]
    videos = analyzer.search_trending_keywords(keywords, max_results=50)
    
    # Analyze patterns
    analysis = analyzer.analyze_trending_patterns(videos)
    
    # Save results
    output_dir = OUTPUTS_DIR / "trend_analysis"
    analyzer.save_analysis(videos, analysis, output_dir)
    
    print(f"Found {len(videos)} trending videos")
    print(f"Analysis saved to: {output_dir}")
