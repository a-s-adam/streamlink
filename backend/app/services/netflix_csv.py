"""Netflix CSV parser service.

This module handles parsing Netflix viewing history CSV files.
"""
import csv
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from io import StringIO

logger = logging.getLogger(__name__)


class NetflixCSVParser:
    """Parser for Netflix viewing history CSV files."""
    
    def parse_csv(self, csv_content: str) -> List[Dict[str, Any]]:
        """Parse Netflix CSV content and return structured data."""
        try:
            # Parse CSV content
            csv_file = StringIO(csv_content)
            reader = csv.DictReader(csv_file)
            
            items = []
            for row in reader:
                try:
                    item = self._parse_row(row)
                    if item:
                        items.append(item)
                except Exception as e:
                    logger.warning(f"Failed to parse row: {row}, error: {e}")
                    continue
            
            logger.info(f"Successfully parsed {len(items)} items from Netflix CSV")
            return items
            
        except Exception as e:
            logger.error(f"Error parsing Netflix CSV: {e}")
            raise
    
    def _parse_row(self, row: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Parse a single CSV row."""
        try:
            # Extract basic information
            title = row.get("Title", "").strip()
            if not title:
                return None
            
            # Parse date
            date_str = row.get("Date", "")
            date = None
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    # Try alternative format
                    try:
                        date = datetime.strptime(date_str, "%m/%d/%Y")
                    except ValueError:
                        logger.warning(f"Could not parse date: {date_str}")
                        date = datetime.utcnow()
            
            # Parse duration
            duration_str = row.get("Duration", "")
            duration_minutes = None
            if duration_str:
                duration_minutes = self._parse_duration(duration_str)
            
            # Determine type (movie vs TV show)
            item_type = "movie"
            if duration_minutes and duration_minutes > 120:  # Over 2 hours likely a movie
                item_type = "movie"
            elif duration_minutes and duration_minutes < 60:  # Under 1 hour likely TV episode
                item_type = "tv_show"
            else:
                item_type = "unknown"
            
            # Extract year from title if present
            year = None
            if "(" in title and ")" in title:
                year_part = title.split("(")[-1].split(")")[0]
                try:
                    year = int(year_part)
                    if year < 1900 or year > 2030:  # Sanity check
                        year = None
                except ValueError:
                    year = None
            
            # Clean title (remove year if present)
            clean_title = title
            if year and f"({year})" in title:
                clean_title = title.replace(f"({year})", "").strip()
            
            return {
                "title": clean_title,
                "year": year,
                "date": date,
                "duration_minutes": duration_minutes,
                "type": item_type,
                "external_id": row.get("Profile Name", ""),  # Use profile as external ID
                "raw_data": row
            }
            
        except Exception as e:
            logger.error(f"Error parsing row {row}: {e}")
            return None
    
    def _parse_duration(self, duration_str: str) -> Optional[int]:
        """Parse duration string to minutes."""
        try:
            duration_str = duration_str.strip().lower()
            
            if "min" in duration_str:
                # Format: "45 min"
                minutes = duration_str.replace("min", "").strip()
                return int(minutes)
            elif ":" in duration_str:
                # Format: "1:30:00" or "45:00"
                parts = duration_str.split(":")
                if len(parts) == 3:
                    # Hours:Minutes:Seconds
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    seconds = int(parts[2])
                    return hours * 60 + minutes + (seconds // 60)
                elif len(parts) == 2:
                    # Minutes:Seconds
                    minutes = int(parts[0])
                    seconds = int(parts[1])
                    return minutes + (seconds // 60)
            else:
                # Try to extract just the number
                import re
                numbers = re.findall(r'\d+', duration_str)
                if numbers:
                    return int(numbers[0])
            
            return None
            
        except Exception as e:
            logger.warning(f"Could not parse duration: {duration_str}, error: {e}")
            return None
