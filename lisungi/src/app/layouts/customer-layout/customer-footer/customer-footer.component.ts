import { Component } from '@angular/core';
import { SettingService } from 'src/app/core/services/setting/setting.service';

@Component({
  selector: 'app-customer-footer',
  templateUrl: './customer-footer.component.html',
  styles: [
  ]
})
export class CustomerFooterComponent {

setting$ = this.settingService.setting$;

  public constructor(
        private settingService: SettingService,
  ){}
}
