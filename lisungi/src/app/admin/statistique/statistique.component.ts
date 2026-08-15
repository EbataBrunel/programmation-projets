import { Component } from '@angular/core';
import { Chart } from 'chart.js/auto';
import { UserProfileService } from 'src/app/core/services/userProfile/user-profile.service';
import { ContributionService } from 'src/app/core/services/contribution/contribution.service';
import { GenderCount } from 'src/app/core/models/GenderCount';
import { ContributionCountByEventType } from 'src/app/core/models/ContributionCountByEventType';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-statistique',
  templateUrl: './statistique.component.html',
  styles: []
})
export class StatistiqueComponent {

  pieChart!: Chart;
  contributionsChart!: Chart;

  genderCounts: GenderCount[] = [];
  contributionsCount: ContributionCountByEventType[] = [];

  constructor(
    private titleService: Title,
    private settingService: SettingService,
    private profileService: UserProfileService,
    private contributionService: ContributionService
  ) {
    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Statistiques | ${setting.nameApp}`);
      }
    });
  }

  ngOnInit(): void {
    this.loadGenderCounts();
    this.loadContributionCounts();
  }

  loadGenderCounts(): void {
    this.profileService.countProfilesByGender().subscribe({
      next: (data) => {
        this.genderCounts = data;

        console.log(
          'Nombre de profils par sexe :',
          this.genderCounts
        );

        this.createPieChart();
      },
      error: (err) => {
        console.error(
          'Erreur lors du chargement des statistiques :',
          err
        );
      }
    });
  }

  loadContributionCounts(): void {
    this.contributionService.getCountContributionsByEventType().subscribe({
      next: (data) => {
        this.contributionsCount = data;

        console.log(
          'Nombre de contributions par type évènement :',
          this.contributionsCount
        );

        this.createContributionsChart();
      },
      error: (err) => {
        console.error(
          'Erreur lors du chargement des contributions :',
          err
        );
      }
    });
  }

  createPieChart(): void {

    const canvas = document.getElementById(
      'pieChart'
    ) as HTMLCanvasElement;

    if (!canvas) {
      console.error('Canvas pieChart introuvable');
      return;
    }

    if (this.pieChart) {
      this.pieChart.destroy();
    }

    this.pieChart = new Chart(canvas, {
      type: 'doughnut',

      data: {
        labels: this.genderCounts.map(
          item => item.gender
        ),

        datasets: [
          {
            data: this.genderCounts.map(
              item => item.count
            )
          }
        ]
      },

      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    });
  }

  createContributionsChart(): void {

    const canvas = document.getElementById(
      'contributionsChart'
    ) as HTMLCanvasElement;

    if (!canvas) {
      console.error('Canvas contributionsChart introuvable');
      return;
    }

    if (this.contributionsChart) {
      this.contributionsChart.destroy();
    }

    this.contributionsChart = new Chart(canvas, {
      type: 'bar',

      data: {
        labels: this.contributionsCount.map(
          item => item.eventTypeName
        ),

        datasets: [
          {
            label: 'Contributions',
            data: this.contributionsCount.map(
              item => item.contributionCount
            )
          }
        ]
      },

      options: {
        responsive: true,
        maintainAspectRatio: false,

        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }
}
