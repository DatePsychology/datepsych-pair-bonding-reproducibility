#!/usr/bin/env python3
"""Regenerate five figures and numerical audit from published summary statistics.

No participant-level data are used. See README.md for provenance and limitations.
Python 3.10+, matplotlib and numpy. Run from any working directory.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = Path(__file__).resolve().parent
NAVY = '#1e3a55'
TEAL = '#24788b'
SLATE = '#667588'
ACCENT = '#b35b46'
SOFT = '#e8edf0'
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.spines.top': False, 'axes.spines.right': False,
    'figure.facecolor': 'white', 'savefig.facecolor': 'white',
})


def read_csv(filename: str) -> list[dict[str, str]]:
    with (HERE / filename).open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def label_axis(ax, title: str, source: str) -> None:
    ax.set_title(title, loc='left', fontsize=15, color=NAVY, weight='bold', pad=16)
    ax.text(0, -.14, source, transform=ax.transAxes,
            fontsize=8.4, color='#536273', va='top')


def save(fig, dest: Path, filename: str) -> None:
    fig.savefig(dest / filename, dpi=180, bbox_inches='tight', pad_inches=.3)
    plt.close(fig)


def figure_1(dest: Path) -> None:
    """Original conceptual causal diagram; arrows are possibilities, not estimates."""
    fig, ax = plt.subplots(figsize=(10.6, 5.4))
    ax.set_xlim(0, 11); ax.set_ylim(0, 6); ax.axis('off')
    boxes = [
        (0.5, 4.15, 3.0, 1.0, 'Pre-existing traits\nand preferences'),
        (0.5, 0.6, 3.0, 1.0, 'Early and ongoing\nsocial context'),
        (4.3, 2.6, 2.65, 1.0, 'Sexual and romantic\nexperiences'),
        (8.05, 2.6, 2.55, 1.0, 'Later relationship\noutcomes'),
    ]
    for x,y,w,h,title in boxes:
        ax.add_patch(FancyBboxPatch((x,y),w,h,
            boxstyle='round,pad=0.1,rounding_size=0.16',
            facecolor='#f0f4f7',edgecolor='#6a8396',linewidth=1.4))
        ax.text(x+w/2,y+h/2,title,ha='center',va='center',fontsize=12,
                weight='medium',color=NAVY)
    def arrow(start,end,rad=0):
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=16,
            connectionstyle=f'arc3,rad={rad}',lw=1.6,color=TEAL))
    arrow((3.4,4.45),(4.45,3.55))
    arrow((3.35,.98),(4.4,2.65))
    arrow((7,3.1),(7.98,3.1))
    arrow((3.48,4.64),(8.55,3.66),-.16)
    arrow((3.42,1.12),(8.28,2.63),.1)
    ax.text(5.3,5.45,
        'Multiple plausible pathways; arrows are hypotheses, not estimated effects',
        ha='center',fontsize=12,color='#3d5364')
    save(fig,dest,'figure_1_causal_paths.png')


def figure_2(dest: Path, rows: list[dict[str,str]]) -> None:
    """Direct transcription of the 18 displayed Harden h² estimates."""
    vals=np.array([float(r['h2_percent']) for r in rows])
    labels=[r['chart_label'] for r in rows]
    fig,ax=plt.subplots(figsize=(11.5,9.4)); yy=np.arange(len(vals))
    ax.axvspan(30,60,color=SOFT,zorder=0)
    ax.axvline(30,lw=1,ls='--',color='#a5b0b8')
    ax.axvline(60,lw=1,ls='--',color='#a5b0b8')
    ax.scatter(vals,yy,s=70,c=[ACCENT if (v<30 or v>60) else TEAL for v in vals],zorder=3)
    for i,v in enumerate(vals):
        ax.text(v+1.1,i,f'{v:g}%',va='center',fontsize=10)
    ax.set_yticks(yy,labels,fontsize=9.4)
    ax.set_xlim(-3,76);ax.set_xlabel('Reported heritability (h²)')
    ax.invert_yaxis();ax.grid(axis='x',alpha=.2)
    label_axis(ax,'The reproduced Harden table is not uniformly 30–60%',
               'Source: Harden (2014), Table 1 (continued); 18 displayed estimates; varied outcomes.')
    save(fig,dest,'figure_2_harden_audit.png')


def figure_3(dest:Path, rows:list[dict[str,str]]) -> None:
    """Approximate confidence intervals on the probit coefficient scale."""
    fig,ax=plt.subplots(figsize=(10.7,4.9));ypos=np.arange(len(rows))[::-1]
    for i,r in enumerate(rows):
        coef=float(r['coefficient']);se=float(r['standard_error']);yy=ypos[i]
        color=TEAL if r['model']=='ordinary probit' else ACCENT
        ax.errorbar(coef,yy,xerr=1.96*se,fmt='o',color=color,
                    ecolor=color,capsize=4,markersize=7,lw=2)
        ax.text(coef,yy+.17,f'{coef:.3f} (SE {se:.3f})',ha='center',
                fontsize=9,color=NAVY)
    ax.set_yticks(ypos,[r['chart_label'] for r in rows])
    ax.axvline(0,c=SLATE,ls='--',lw=1.1);ax.set_xlim(-2.2,1.7)
    ax.set_xlabel('Probit coefficient for virginity at marriage (relative to nonvirginity)')
    ax.grid(axis='x',alpha=.17)
    label_axis(ax,'Kahn & London: uncertainty rises in the selection model',
               '95% intervals are approximate: coefficient ± 1.96 × SE; Tables 3–4, 1991.')
    save(fig,dest,'figure_3_kahn_uncertainty.png')


def figure_4(dest:Path, rows:list[dict[str,str]]) -> None:
    """Published point estimates only. Do not infer absolute divorce probability."""
    vals=[float(r['exponentiated_estimate']) for r in rows]
    names=[r['chart_label'].replace('\\n','\n') for r in rows]
    fig,ax=plt.subplots(figsize=(9.1,5.1))
    bars=ax.bar(names,vals,width=.55,color=[SLATE]+[TEAL]*(len(rows)-1))
    ax.set_ylim(0,3.7)
    ax.set_ylabel('Exponentiated model coefficient (reference = 1.00)')
    for b,v in zip(bars,vals):
        ax.text(b.get_x()+b.get_width()/2,v+.09,f'{v:.2f}',ha='center',
                fontsize=13,weight='bold',color=NAVY)
    label_axis(ax,'Add Health: prior nonspousal partners and marital dissolution',
               'Smith & Wolfinger (2024), Table 4, Model 3; assessed at Wave III; associations, not causal effects.')
    save(fig,dest,'figure_4_add_health.png')


def figure_5(dest:Path, rows:list[dict[str,str]]) -> None:
    """Reported frequencies for different sexual-event contexts."""
    vals=[float(r['reported_orgasm_percent']) for r in rows]
    names=[r['chart_label'].replace('\\n','\n') for r in rows]
    fig,ax=plt.subplots(figsize=(9.2,5.2))
    bars=ax.bar(names,vals,color=[SLATE,SLATE,TEAL,TEAL],width=.62)
    ax.set_ylim(0,78);ax.set_ylabel('Sexual events with reported orgasm (%)')
    for b,v in zip(bars,vals):
        ax.text(b.get_x()+b.get_width()/2,v+1.3,f'{v:g}%',ha='center',
                fontsize=12,weight='bold',color=NAVY)
    label_axis(ax,'The 11% estimate refers to first hookups—not all casual sex',
               'Armstrong, England & Fogarty (2012), Figure 1; heterosexual college women.')
    save(fig,dest,'figure_5_armstrong.png')


def assert_input_integrity(harden,kahn,addhealth,armstrong):
    assert len(harden)==18, 'Harden figure must have 18 original table rows'
    hv=[float(r['h2_percent']) for r in harden]
    assert sum(v<30 for v in hv)==4 and sum(v>60 for v in hv)==1
    assert min(hv)==0 and max(hv)==65
    assert len(kahn)==4
    assert [float(r['coefficient']) for r in kahn]==[-.601,-.511,-.402,-.274]
    assert [float(r['standard_error']) for r in kahn]==[.078,.514,.098,.842]
    assert [float(r['exponentiated_estimate']) for r in addhealth]==[1.00,1.64,3.20]
    assert [float(r['reported_orgasm_percent']) for r in armstrong]==[11.,16.,34.,67.]


def calculate_results(harden,kahn,addhealth,armstrong)->str:
    vals=np.array([float(r['h2_percent']) for r in harden])
    cvals=[float(r['c2_percent']) for r in harden]
    lines=[
        'PAIR BONDING: REPRODUCED NUMERICAL AUDIT (v1)',
        'Based only on manually transcribed published summary statistics; not an individual-level replication.',
        '', 'HARDEN (2014), TABLE 1 CONTINUED — 18 DISPLAYED ROWS',
        f'Count: {len(vals)}; min h²: {min(vals):g}%; max h²: {max(vals):g}%',
        f'h² <30%: {sum(vals<30)}; 30–60% inclusive: {sum((vals>=30)&(vals<=60))}; h² >60%: {sum(vals>60)}',
        f'Risky sexual behavior: h²={harden[4]["h2_percent"]}%, c²={harden[4]["c2_percent"]}%',
        f'Mean h² across these heterogeneous rows: deliberately not calculated (not a meta-analysis).',
        '', 'KAHN & LONDON (1991), TABLES 3 AND 4',
        'Approximate normal-theory 95% confidence intervals, not author-provided intervals:',
    ]
    for r in kahn:
        b=float(r['coefficient']);se=float(r['standard_error'])
        lines.append(f'  {r["chart_label"]}: coefficient {b:+.3f}; SE {se:.3f}; 95% approx CI [{b-1.96*se:+.3f}, {b+1.96*se:+.3f}]')
    lines += [
        f'First five years: bivariate/ordinary SE ratio = {float(kahn[1]["standard_error"])/float(kahn[0]["standard_error"]):.2f}x',
        f'Years five–ten: bivariate/ordinary SE ratio = {float(kahn[3]["standard_error"])/float(kahn[2]["standard_error"]):.2f}x',
        'Reported residual error correlations: -0.054 (first five years); -0.079 (years five–ten).',
        'These correlations were reported as statistically nonsignificant.',
        'Coefficient sign: negative for virgin at marriage versus nonvirgin.',
        'Loss of statistical significance DOES NOT prove a zero effect or that selection explained the association.',
        '', 'SMITH & WOLFINGER (2024), TABLE 4 MODEL 3',
    ]
    for r in addhealth:
        lines.append(f'  {r["group"]}: {float(r["exponentiated_estimate"]):.2f}')
    lines+=['This is an adjusted association in the later-marrying Add Health subsample (N=3506).',
            'Reference is zero prior nonspousal partners; groups are estimated, partly data-driven.',
            'No absolute risk or causal inference follows from these point estimates.',
            '', 'ARMSTRONG ET AL. (2012), FIGURE 1']
    for r in armstrong:
        lines.append(f'  {r["context"]}: {float(r["reported_orgasm_percent"]):g}%')
    lines += ['', 'Figure 1 is conceptual, not fitted to empirical data.',
              'Generated figures are reconstructions from article-level published numbers, not replication of original analyses.','']
    return '\n'.join(lines)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir',type=Path,default=HERE,help='Directory for figures and output .txt (defaults to repository root)')
    args=ap.parse_args();dest=args.output_dir.expanduser().resolve();dest.mkdir(parents=True,exist_ok=True)
    harden=read_csv('harden_heritability_inputs.csv')
    kahn=read_csv('kahn_london_probit_inputs.csv')
    addhealth=read_csv('smith_wolfinger_add_health_inputs.csv')
    armstrong=read_csv('armstrong_orgasm_inputs.csv')
    assert_input_integrity(harden,kahn,addhealth,armstrong)
    figure_1(dest);figure_2(dest,harden);figure_3(dest,kahn)
    figure_4(dest,addhealth);figure_5(dest,armstrong)
    output=calculate_results(harden,kahn,addhealth,armstrong)
    (dest/'reconstruction_results_v1.txt').write_text(output,encoding='utf-8')
    print(output)
    print(f'Five figures + results written to {dest}')

if __name__=='__main__':
    main()
