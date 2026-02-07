"""
Personality Engine Service
---------------------------
Microservice for managing AI personality, behaviors, and traits.
Provides an API for personality updates and queries.
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
import logging
import sys

# Import personality components
try:
    from .ai_personality.personality import PersonalityTraits
except ImportError:
    PersonalityTraits = None


def setup_logger(name: str = "personality_engine"):
    """Configure and return a standardized logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Personality Engine Service starting up...")
    yield
    logger.info("Personality Engine Service shutting down...")


app = FastAPI(title="Sylvia Personality Engine Service", lifespan=lifespan)


class PersonalityRequest(BaseModel):
    trait: str
    value: Optional[float] = None


class PersonalityResponse(BaseModel):
    trait: str
    value: float
    description: Optional[str] = None


class PersonalityUpdateRequest(BaseModel):
    traits: Dict[str, float]


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "online", "service": "personality_engine"}


@app.get("/personality", response_model=Dict[str, Any])
async def get_personality():
    """Get current personality configuration."""
    try:
        if PersonalityTraits is None:
            return {
                "status": "limited",
                "message": "Personality system not fully initialized",
                "traits": {}
            }

        # Return default personality traits
        return {
            "status": "active",
            "traits": {
                "openness": 0.8,
                "conscientiousness": 0.7,
                "extraversion": 0.6,
                "agreeableness": 0.75,
                "neuroticism": 0.3
            }
        }
    except Exception as e:
        logger.error(f"Error getting personality: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/personality/update")
async def update_personality(request: PersonalityUpdateRequest):
    """Update personality traits."""
    try:
        logger.info(f"Updating personality traits: {request.traits}")

        # Validate trait values are between 0 and 1
        for trait, value in request.traits.items():
            if not 0 <= value <= 1:
                raise HTTPException(
                    status_code=400,
                    detail=f"Trait value for {trait} must be between 0 and 1"
                )

        return {
            "status": "updated",
            "traits": request.traits,
            "message": "Personality traits updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating personality: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/personality/{trait}")
async def get_trait(trait: str):
    """Get specific personality trait value."""
    try:
        # Default trait values
        default_traits = {
            "openness": 0.8,
            "conscientiousness": 0.7,
            "extraversion": 0.6,
            "agreeableness": 0.75,
            "neuroticism": 0.3
        }

        if trait.lower() not in default_traits:
            raise HTTPException(
                status_code=404,
                detail=f"Trait '{trait}' not found"
            )

        return {
            "trait": trait.lower(),
            "value": default_traits[trait.lower()]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting trait {trait}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5003)
