import { Component } from '@angular/core';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { Setting } from 'src/app/core/models/Setting';

@Component({
  selector: 'app-customer-header',
  templateUrl: './customer-header.component.html',
  styleUrls: ['./customer-header.component.css']
})
export class CustomerHeaderComponent {

    error: string = '';
    setting$ = this.settingService.setting$;

    constructor(
      private settingService: SettingService
    ){}

    menuOpen = false;


    toggleMenu(): void {
      this.menuOpen = !this.menuOpen;
    }


}
