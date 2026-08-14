import { Component } from '@angular/core';
import { SettingService } from 'src/app/core/services/setting/setting.service';

@Component({
  selector: 'app-admin-footer',
  templateUrl: './admin-footer.component.html',
  styles: [
  ]
})
export class AdminFooterComponent {

  setting$ = this.settingService.setting$;

  constructor(private settingService: SettingService){}

}
