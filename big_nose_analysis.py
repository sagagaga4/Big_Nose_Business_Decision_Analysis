"""
Comprehensive Business Analysis for Big Nose Artist
From Raw Data to Business Insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for professional visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Configuration
DATA_DIR = "***"
OUTPUT_DIR = "***"

import os
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("="*80)
print("BIG NOSE ARTIST - COMPREHENSIVE BUSINESS ANALYSIS")
print("="*80)
print("\nLoading and processing data...\n")

# ============================================================================
# PART 1: DATA LOADING & CLEANING
# ============================================================================

# Load earnings per song data
earnings_df = pd.read_csv(f"{DATA_DIR}/Earnings_Per_Songs/Big Nose-earnings-per-song.csv")
print(f"✓ Loaded earnings data: {len(earnings_df)} songs")

# Load songs 1 year performance data
songs_1year_df = pd.read_csv(f"{DATA_DIR}/Spotify_Analysis/Big Nose-songs-1year.csv")
print(f"✓ Loaded 1-year songs data: {len(songs_1year_df)} songs")

# Load audience timeline data
audience_df = pd.read_csv(f"{DATA_DIR}/Spotify_Analysis/Big Nose-audience-timeline.csv")
audience_df['date'] = pd.to_datetime(audience_df['date'])
print(f"✓ Loaded audience timeline: {len(audience_df)} days")

# Load playlists data
playlists_df = pd.read_csv(f"{DATA_DIR}/Spotify_Analysis/Big Nose-playlists-1year.csv")
print(f"✓ Loaded playlists data: {len(playlists_df)} playlists")

# Load all songs data
songs_all_df = pd.read_csv(f"{DATA_DIR}/Earnings_Per_Songs/Big Nose-songs-all.csv")
print(f"✓ Loaded all songs data: {len(songs_all_df)} songs")

# ============================================================================
# DATA CLEANING & PREPARATION
# ============================================================================

print("\n" + "="*80)
print("DATA QUALITY ASSESSMENT")
print("="*80)

# Clean earnings data
earnings_df['release_date'] = pd.to_datetime(earnings_df['release_date'], errors='coerce')
earnings_df['Amount'] = earnings_df['Amount'].astype(str).str.replace('$', '').str.replace(',', '').astype(float)
earnings_df['listeners'] = pd.to_numeric(earnings_df['listeners'], errors='coerce')
earnings_df['streams'] = pd.to_numeric(earnings_df['streams'], errors='coerce')
earnings_df['saves'] = pd.to_numeric(earnings_df['saves'], errors='coerce')

# Filter to Big Nose songs only (exclude collaborations where Big Nose is not primary)
earnings_df = earnings_df[earnings_df['Artist'].str.contains('Big Nose', na=False)]

# Calculate years since release
earnings_df['years_since_release'] = (datetime.now() - earnings_df['release_date']).dt.days / 365.25
earnings_df['release_year'] = earnings_df['release_date'].dt.year

# Data quality metrics
print(f"\n1. Earnings Data Quality:")
print(f"   - Total songs: {len(earnings_df)}")
print(f"   - Missing release dates: {earnings_df['release_date'].isna().sum()}")
print(f"   - Missing amounts: {earnings_df['Amount'].isna().sum()}")
print(f"   - Date range: {earnings_df['release_date'].min()} to {earnings_df['release_date'].max()}")
print(f"   - Total earnings: ${earnings_df['Amount'].sum():,.2f}")

print(f"\n2. Audience Timeline Data Quality:")
print(f"   - Date range: {audience_df['date'].min()} to {audience_df['date'].max()}")
print(f"   - Missing listeners: {audience_df['listeners'].isna().sum()}")
print(f"   - Missing streams: {audience_df['streams'].isna().sum()}")
print(f"   - Missing followers: {audience_df['followers'].isna().sum()}")

print(f"\n3. Songs 1-Year Data Quality:")
print(f"   - Total songs: {len(songs_1year_df)}")
print(f"   - Total streams (1 year): {songs_1year_df['streams'].sum():,}")
print(f"   - Total listeners (1 year): {songs_1year_df['listeners'].sum():,}")
print(f"   - Total saves (1 year): {songs_1year_df['saves'].sum():,}")

# ============================================================================
# PART 2: EXPLORATORY DATA ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("EXPLORATORY DATA ANALYSIS")
print("="*80)

# Calculate key metrics
total_earnings = earnings_df['Amount'].sum()
avg_earnings_per_song = earnings_df['Amount'].mean()
median_earnings_per_song = earnings_df['Amount'].median()

print(f"\nKey Financial Metrics:")
print(f"   - Total Earnings: ${total_earnings:,.2f}")
print(f"   - Average per song: ${avg_earnings_per_song:,.2f}")
print(f"   - Median per song: ${median_earnings_per_song:,.2f}")
print(f"   - Top 5 songs account for: ${earnings_df.nlargest(5, 'Amount')['Amount'].sum():,.2f} ({earnings_df.nlargest(5, 'Amount')['Amount'].sum()/total_earnings*100:.1f}%)")

# Top performing songs
top_songs = earnings_df.nlargest(10, 'Amount')[['Song Title', 'Amount', 'listeners', 'streams', 'saves', 'release_date']]
print(f"\nTop 10 Earning Songs:")
for idx, row in top_songs.iterrows():
    print(f"   {row['Song Title']}: ${row['Amount']:.2f} ({row['streams']:,.0f} streams)")

# ============================================================================
# PART 3: EARNINGS ANALYSIS (5 YEARS)
# ============================================================================

print("\n" + "="*80)
print("EARNINGS ANALYSIS - 5 YEAR TREND")
print("="*80)

# Filter to last 5 years
five_years_ago = datetime.now() - timedelta(days=5*365)
earnings_5yr = earnings_df[earnings_df['release_date'] >= five_years_ago].copy()

# Group by year
earnings_by_year = earnings_5yr.groupby('release_year').agg({
    'Amount': 'sum',
    'Song Title': 'count',
    'streams': 'sum',
    'listeners': 'sum',
    'saves': 'sum'
}).rename(columns={'Song Title': 'song_count'})

print(f"\nEarnings by Year (Last 5 Years):")
for year, row in earnings_by_year.iterrows():
    print(f"   {year}: ${row['Amount']:,.2f} ({row['song_count']} songs, {row['streams']:,.0f} streams)")

# Calculate growth rates
if len(earnings_by_year) > 1:
    years = sorted(earnings_by_year.index)
    for i in range(1, len(years)):
        prev_earnings = earnings_by_year.loc[years[i-1], 'Amount']
        curr_earnings = earnings_by_year.loc[years[i], 'Amount']
        growth = ((curr_earnings - prev_earnings) / prev_earnings * 100) if prev_earnings > 0 else 0
        print(f"   {years[i-1]} to {years[i]}: {growth:+.1f}% earnings growth")

# ============================================================================
# PART 4: FOLLOWER GROWTH ANALYSIS (LAST YEAR)
# ============================================================================

print("\n" + "="*80)
print("FOLLOWER GROWTH ANALYSIS - LAST YEAR")
print("="*80)

# Filter to last year
one_year_ago = datetime.now() - timedelta(days=365)
audience_1yr = audience_df[audience_df['date'] >= one_year_ago].copy()

# Calculate follower growth
initial_followers = audience_1yr['followers'].iloc[0] if len(audience_1yr) > 0 else 0
final_followers = audience_1yr['followers'].iloc[-1] if len(audience_1yr) > 0 else 0
follower_growth = final_followers - initial_followers
follower_growth_pct = (follower_growth / initial_followers * 100) if initial_followers > 0 else 0

print(f"\nFollower Growth Metrics:")
print(f"   - Starting followers (1 year ago): {initial_followers:,}")
print(f"   - Current followers: {final_followers:,}")
print(f"   - Net growth: {follower_growth:+,}")
print(f"   - Growth rate: {follower_growth_pct:+.1f}%")

# Monthly follower growth
audience_1yr['year_month'] = audience_1yr['date'].dt.to_period('M')
monthly_followers = audience_1yr.groupby('year_month')['followers'].last()
print(f"\nMonthly Follower Count:")
for month, followers in monthly_followers.items():
    print(f"   {month}: {followers:,}")

# ============================================================================
# PART 5: PERFORMANCE METRICS (LAST YEAR)
# ============================================================================

print("\n" + "="*80)
print("PERFORMANCE METRICS - LAST YEAR")
print("="*80)

# Aggregate metrics from songs 1 year data
total_streams_1yr = songs_1year_df['streams'].sum()
total_listeners_1yr = songs_1year_df['listeners'].sum()
total_saves_1yr = songs_1year_df['saves'].sum()

print(f"\n1-Year Performance Summary:")
print(f"   - Total Streams: {total_streams_1yr:,}")
print(f"   - Total Listeners: {total_listeners_1yr:,}")
print(f"   - Total Saves: {total_saves_1yr:,}")
print(f"   - Average streams per song: {total_streams_1yr / len(songs_1year_df):,.0f}")
print(f"   - Save rate: {(total_saves_1yr / total_streams_1yr * 100):.2f}%")

# Top performing songs in last year
top_performers_1yr = songs_1year_df.nlargest(10, 'streams')
print(f"\nTop 10 Performing Songs (Last Year):")
for idx, row in top_performers_1yr.iterrows():
    print(f"   {row['song']}: {row['streams']:,} streams, {row['listeners']:,} listeners, {row['saves']} saves")

# ============================================================================
# PART 6: RECENT METRICS ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("RECENT METRICS ANALYSIS (Last 28 Days)")
print("="*80)

# User provided metrics
monthly_active_listeners = 733
previously_active_listeners = 12766
programmed_listeners = 205368

total_reach = monthly_active_listeners + previously_active_listeners + programmed_listeners

print(f"\nListener Categories (Last 28 Days):")
print(f"   - Monthly Active Listeners: {monthly_active_listeners:,}")
print(f"   - Previously Active Listeners: {previously_active_listeners:,}")
print(f"   - Programmed Listeners: {programmed_listeners:,}")
print(f"   - Total Reach: {total_reach:,}")

# Calculate engagement metrics
engagement_rate = (monthly_active_listeners / total_reach * 100) if total_reach > 0 else 0
organic_rate = ((monthly_active_listeners + previously_active_listeners) / total_reach * 100) if total_reach > 0 else 0

print(f"\nEngagement Analysis:")
print(f"   - Engagement Rate (Active/Total): {engagement_rate:.2f}%")
print(f"   - Organic Engagement Rate: {organic_rate:.2f}%")
print(f"   - Programmed vs Organic Ratio: {programmed_listeners / (monthly_active_listeners + previously_active_listeners):.2f}x")

# ============================================================================
# PART 7: VISUALIZATIONS
# ============================================================================

print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

# Create figure with multiple subplots
fig = plt.figure(figsize=(20, 24))

# 1. Earnings Over Time (5 years)
ax1 = plt.subplot(4, 2, 1)
earnings_by_year_plot = earnings_5yr.groupby('release_year')['Amount'].sum()
ax1.bar(earnings_by_year_plot.index, earnings_by_year_plot.values, color='#2ecc71')
ax1.set_title('Total Earnings by Release Year (Last 5 Years)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Year')
ax1.set_ylabel('Earnings ($)')
ax1.grid(True, alpha=0.3)
for i, v in enumerate(earnings_by_year_plot.values):
    ax1.text(earnings_by_year_plot.index[i], v, f'${v:,.0f}', ha='center', va='bottom', fontsize=9)

# 2. Top Earning Songs
ax2 = plt.subplot(4, 2, 2)
top_10_earnings = earnings_df.nlargest(10, 'Amount')
ax2.barh(range(len(top_10_earnings)), top_10_earnings['Amount'].values, color='#3498db')
ax2.set_yticks(range(len(top_10_earnings)))
ax2.set_yticklabels([s[:30] + '...' if len(s) > 30 else s for s in top_10_earnings['Song Title'].values], fontsize=8)
ax2.set_title('Top 10 Earning Songs (All Time)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Earnings ($)')
ax2.grid(True, alpha=0.3, axis='x')

# 3. Follower Growth Over Time
ax3 = plt.subplot(4, 2, 3)
audience_1yr_sampled = audience_1yr[::7]  # Sample weekly for clarity
ax3.plot(audience_1yr_sampled['date'], audience_1yr_sampled['followers'], linewidth=2, color='#e74c3c')
ax3.set_title('Follower Growth (Last Year)', fontsize=14, fontweight='bold')
ax3.set_xlabel('Date')
ax3.set_ylabel('Followers')
ax3.grid(True, alpha=0.3)
ax3.tick_params(axis='x', rotation=45)

# 4. Streams Over Time (Last Year)
ax4 = plt.subplot(4, 2, 4)
audience_1yr_sampled = audience_1yr[::7]
ax4.plot(audience_1yr_sampled['date'], audience_1yr_sampled['streams'], linewidth=2, color='#9b59b6')
ax4.set_title('Daily Streams (Last Year)', fontsize=14, fontweight='bold')
ax4.set_xlabel('Date')
ax4.set_ylabel('Streams')
ax4.grid(True, alpha=0.3)
ax4.tick_params(axis='x', rotation=45)

# 5. Top Performing Songs (1 Year)
ax5 = plt.subplot(4, 2, 5)
top_10_streams = songs_1year_df.nlargest(10, 'streams')
ax5.barh(range(len(top_10_streams)), top_10_streams['streams'].values, color='#f39c12')
ax5.set_yticks(range(len(top_10_streams)))
ax5.set_yticklabels([s[:30] + '...' if len(s) > 30 else s for s in top_10_streams['song'].values], fontsize=8)
ax5.set_title('Top 10 Songs by Streams (Last Year)', fontsize=14, fontweight='bold')
ax5.set_xlabel('Streams')
ax5.grid(True, alpha=0.3, axis='x')

# 6. Earnings vs Streams Correlation
ax6 = plt.subplot(4, 2, 6)
# Merge earnings with streams data
earnings_with_streams = earnings_df[earnings_df['streams'].notna() & (earnings_df['streams'] > 0)]
if len(earnings_with_streams) > 0:
    ax6.scatter(earnings_with_streams['streams'], earnings_with_streams['Amount'], alpha=0.6, s=50, color='#1abc9c')
    ax6.set_title('Earnings vs Streams Correlation', fontsize=14, fontweight='bold')
    ax6.set_xlabel('Streams')
    ax6.set_ylabel('Earnings ($)')
    ax6.set_xscale('log')
    ax6.grid(True, alpha=0.3)

# 7. Listener Categories (Recent)
ax7 = plt.subplot(4, 2, 7)
categories = ['Monthly Active', 'Previously Active', 'Programmed']
values = [monthly_active_listeners, previously_active_listeners, programmed_listeners]
colors = ['#2ecc71', '#3498db', '#95a5a6']
ax7.pie(values, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
ax7.set_title('Listener Distribution (Last 28 Days)', fontsize=14, fontweight='bold')

# 8. Songs Released Over Time
ax8 = plt.subplot(4, 2, 8)
songs_by_year = earnings_df.groupby('release_year').size()
ax8.bar(songs_by_year.index, songs_by_year.values, color='#e67e22')
ax8.set_title('Number of Songs Released by Year', fontsize=14, fontweight='bold')
ax8.set_xlabel('Year')
ax8.set_ylabel('Number of Songs')
ax8.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/comprehensive_analysis.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved visualization: {OUTPUT_DIR}/comprehensive_analysis.png")

# ============================================================================
# PART 8: BUSINESS INSIGHTS & RECOMMENDATIONS
# ============================================================================

print("\n" + "="*80)
print("BUSINESS INSIGHTS & ANALYSIS")
print("="*80)

insights = []

# Insight 1: Earnings Concentration
top_5_pct = (earnings_df.nlargest(5, 'Amount')['Amount'].sum() / total_earnings * 100)
insights.append({
    'category': 'Revenue Concentration',
    'finding': f'Top 5 songs generate {top_5_pct:.1f}% of total earnings',
    'implication': 'High dependency on few hits; need diversification strategy'
})

# Insight 2: Follower Growth
if follower_growth_pct > 0:
    insights.append({
        'category': 'Audience Growth',
        'finding': f'Follower growth of {follower_growth_pct:.1f}% in last year',
        'implication': 'Positive growth trajectory; maintain engagement strategies'
    })
else:
    insights.append({
        'category': 'Audience Growth',
        'finding': f'Follower decline of {abs(follower_growth_pct):.1f}% in last year',
        'implication': 'Need to revitalize audience acquisition and retention'
    })

# Insight 3: Engagement Analysis
if engagement_rate < 1:
    insights.append({
        'category': 'Engagement',
        'finding': f'Low engagement rate ({engagement_rate:.2f}%) - high programmed listener ratio',
        'implication': 'Focus on converting programmed listeners to active fans'
    })

# Insight 4: Content Velocity
songs_per_year = earnings_df.groupby('release_year').size().mean()
insights.append({
    'category': 'Content Strategy',
    'finding': f'Average {songs_per_year:.1f} songs released per year',
    'implication': 'Maintain consistent release schedule to build momentum'
})

# Insight 5: Save Rate
save_rate = (total_saves_1yr / total_streams_1yr * 100) if total_streams_1yr > 0 else 0
insights.append({
    'category': 'Fan Engagement',
    'finding': f'Save rate of {save_rate:.2f}% indicates moderate fan loyalty',
    'implication': 'Improve save rate through better song quality and marketing'
})

print("\nKey Insights:")
for i, insight in enumerate(insights, 1):
    print(f"\n{i}. {insight['category']}")
    print(f"   Finding: {insight['finding']}")
    print(f"   Implication: {insight['implication']}")

# ============================================================================
# PART 9: RECOMMENDATIONS
# ============================================================================

print("\n" + "="*80)
print("STRATEGIC RECOMMENDATIONS")
print("="*80)

recommendations = []

# Recommendation 1: Revenue Diversification
recommendations.append({
    'priority': 'HIGH',
    'title': 'Diversify Revenue Streams',
    'description': f'Top 5 songs account for {top_5_pct:.1f}% of earnings. Focus on promoting mid-tier songs and creating new hits.',
    'expected_impact': 'Reduce revenue risk by 30-40%',
    'timeline': '3-6 months'
})

# Recommendation 2: Audience Engagement
if engagement_rate < 1:
    recommendations.append({
        'priority': 'HIGH',
        'title': 'Convert Programmed Listeners to Active Fans',
        'description': f'Only {engagement_rate:.2f}% monthly active engagement. Implement playlist optimization and social media campaigns.',
        'expected_impact': 'Increase active listeners by 50-100%',
        'timeline': '2-4 months'
    })

# Recommendation 3: Content Strategy
recommendations.append({
    'priority': 'MEDIUM',
    'title': 'Maintain Consistent Release Schedule',
    'description': f'Current average of {songs_per_year:.1f} songs/year. Aim for monthly releases to maintain momentum.',
    'expected_impact': 'Increase streams by 20-30%',
    'timeline': 'Ongoing'
})

# Recommendation 4: Playlist Optimization
top_playlist_streams = playlists_df['streams'].sum()
recommendations.append({
    'priority': 'MEDIUM',
    'title': 'Leverage Playlist Placements',
    'description': f'Currently featured in {len(playlists_df)} playlists generating {top_playlist_streams:,} streams. Focus on getting into larger playlists.',
    'expected_impact': 'Increase reach by 40-60%',
    'timeline': '3-6 months'
})

# Recommendation 5: Data-Driven Song Promotion
recommendations.append({
    'priority': 'MEDIUM',
    'title': 'Promote High-Potential Songs',
    'description': f'Identify songs with high save rates but low streams. These indicate strong fan interest that can be amplified.',
    'expected_impact': 'Increase streams for selected songs by 100-200%',
    'timeline': '1-3 months'
})

print("\nPrioritized Recommendations:")
for i, rec in enumerate(recommendations, 1):
    print(f"\n{i}. [{rec['priority']}] {rec['title']}")
    print(f"   Description: {rec['description']}")
    print(f"   Expected Impact: {rec['expected_impact']}")
    print(f"   Timeline: {rec['timeline']}")

# ============================================================================
# PART 10: UPCOMING ARTIST ASSESSMENT
# ============================================================================

print("\n" + "="*80)
print("UPCOMING ARTIST ASSESSMENT")
print("="*80)

assessment_score = 0
max_score = 10
assessment_factors = []

# Factor 1: Follower Growth
if follower_growth_pct > 20:
    score = 2
    assessment_factors.append(('Strong Follower Growth', score, 'Excellent growth trajectory'))
elif follower_growth_pct > 10:
    score = 1.5
    assessment_factors.append(('Moderate Follower Growth', score, 'Positive growth'))
elif follower_growth_pct > 0:
    score = 1
    assessment_factors.append(('Slow Follower Growth', score, 'Needs improvement'))
else:
    score = 0
    assessment_factors.append(('Declining Followers', score, 'Critical issue'))
assessment_score += score

# Factor 2: Stream Volume
if total_streams_1yr > 500000:
    score = 2
    assessment_factors.append(('High Stream Volume', score, 'Strong performance'))
elif total_streams_1yr > 200000:
    score = 1.5
    assessment_factors.append(('Moderate Stream Volume', score, 'Good performance'))
elif total_streams_1yr > 100000:
    score = 1
    assessment_factors.append(('Low Stream Volume', score, 'Needs growth'))
else:
    score = 0.5
    assessment_factors.append(('Very Low Stream Volume', score, 'Critical issue'))
assessment_score += score

# Factor 3: Engagement Rate
if engagement_rate > 2:
    score = 2
    assessment_factors.append(('High Engagement', score, 'Strong fan base'))
elif engagement_rate > 1:
    score = 1.5
    assessment_factors.append(('Moderate Engagement', score, 'Room for improvement'))
elif engagement_rate > 0.5:
    score = 1
    assessment_factors.append(('Low Engagement', score, 'Needs focus'))
else:
    score = 0.5
    assessment_factors.append(('Very Low Engagement', score, 'Critical issue'))
assessment_score += score

# Factor 4: Revenue Generation
if total_earnings > 2000:
    score = 2
    assessment_factors.append(('Strong Revenue', score, 'Monetization working'))
elif total_earnings > 1000:
    score = 1.5
    assessment_factors.append(('Moderate Revenue', score, 'Growing monetization'))
elif total_earnings > 500:
    score = 1
    assessment_factors.append(('Low Revenue', score, 'Needs improvement'))
else:
    score = 0.5
    assessment_factors.append(('Very Low Revenue', score, 'Critical issue'))
assessment_score += score

# Factor 5: Content Consistency
if songs_per_year >= 12:
    score = 2
    assessment_factors.append(('High Content Velocity', score, 'Excellent consistency'))
elif songs_per_year >= 6:
    score = 1.5
    assessment_factors.append(('Moderate Content Velocity', score, 'Good consistency'))
elif songs_per_year >= 3:
    score = 1
    assessment_factors.append(('Low Content Velocity', score, 'Needs more releases'))
else:
    score = 0.5
    assessment_factors.append(('Very Low Content Velocity', score, 'Critical issue'))
assessment_score += score

# Overall Assessment
assessment_pct = (assessment_score / max_score) * 100

print(f"\nAssessment Factors:")
for factor, score, note in assessment_factors:
    print(f"   • {factor}: {score}/2.0 - {note}")

print(f"\n{'='*80}")
print(f"OVERALL ASSESSMENT SCORE: {assessment_score:.1f}/10.0 ({assessment_pct:.1f}%)")
print(f"{'='*80}")

if assessment_pct >= 70:
    verdict = "STRONG UPCOMING ARTIST"
    verdict_desc = "Big Nose demonstrates strong indicators of an upcoming artist with solid growth potential. The artist shows consistent content creation, growing audience, and monetization success."
elif assessment_pct >= 50:
    verdict = "PROMISING UPCOMING ARTIST"
    verdict_desc = "Big Nose shows promise as an upcoming artist with several positive indicators. However, there are areas that need attention to accelerate growth."
elif assessment_pct >= 30:
    verdict = "EMERGING ARTIST"
    verdict_desc = "Big Nose is an emerging artist with potential, but requires strategic focus on key growth areas to reach upcoming artist status."
else:
    verdict = "EARLY STAGE ARTIST"
    verdict_desc = "Big Nose is in early stages of development. Significant strategic improvements are needed across multiple areas."

print(f"\nVERDICT: {verdict}")
print(f"\n{verdict_desc}")

# ============================================================================
# PART 11: EXPORT SUMMARY REPORT
# ============================================================================

print("\n" + "="*80)
print("GENERATING SUMMARY REPORT")
print("="*80)

# Create summary report
report = f"""
BIG NOSE ARTIST - COMPREHENSIVE BUSINESS ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

EXECUTIVE SUMMARY
-----------------
Artist: Big Nose
Analysis Period: Last 5 years (earnings), Last 1 year (performance)
Assessment: {verdict} ({assessment_score:.1f}/10.0)

KEY METRICS
-----------
Total Earnings (All Time): ${total_earnings:,.2f}
Total Streams (Last Year): {total_streams_1yr:,}
Total Listeners (Last Year): {total_listeners_1yr:,}
Total Followers (Current): {final_followers:,}
Follower Growth (Last Year): {follower_growth:+,} ({follower_growth_pct:+.1f}%)

RECENT METRICS (Last 28 Days)
------------------------------
Monthly Active Listeners: {monthly_active_listeners:,}
Previously Active Listeners: {previously_active_listeners:,}
Programmed Listeners: {programmed_listeners:,}
Total Reach: {total_reach:,}
Engagement Rate: {engagement_rate:.2f}%

TOP PERFORMING SONGS (Earnings)
--------------------------------
"""
for idx, row in top_songs.head(5).iterrows():
    report += f"{row['Song Title']}: ${row['Amount']:.2f} ({row['streams']:,.0f} streams)\n"

report += f"""
KEY INSIGHTS
------------
"""
for i, insight in enumerate(insights, 1):
    report += f"{i}. {insight['category']}: {insight['finding']}\n   → {insight['implication']}\n\n"

report += f"""
STRATEGIC RECOMMENDATIONS
--------------------------
"""
for i, rec in enumerate(recommendations, 1):
    report += f"{i}. [{rec['priority']}] {rec['title']}\n"
    report += f"   {rec['description']}\n"
    report += f"   Expected Impact: {rec['expected_impact']}\n"
    report += f"   Timeline: {rec['timeline']}\n\n"

report += f"""
ASSESSMENT CONCLUSION
----------------------
{verdict_desc}

Overall Score: {assessment_score:.1f}/10.0 ({assessment_pct:.1f}%)

{'='*80}
"""

# Save report
with open(f'{OUTPUT_DIR}/analysis_report.txt', 'w') as f:
    f.write(report)

print(f"✓ Saved report: {OUTPUT_DIR}/analysis_report.txt")

# Save detailed data exports
earnings_df.to_csv(f'{OUTPUT_DIR}/earnings_analysis.csv', index=False)
audience_1yr.to_csv(f'{OUTPUT_DIR}/audience_1year.csv', index=False)

print(f"\n{'='*80}")
print("ANALYSIS COMPLETE!")
print(f"{'='*80}")
print(f"\nOutput files saved to: {OUTPUT_DIR}/")
print(f"  - comprehensive_analysis.png (visualizations)")
print(f"  - analysis_report.txt (summary report)")
print(f"  - earnings_analysis.csv (detailed earnings data)")
print(f"  - audience_1year.csv (audience timeline data)")

