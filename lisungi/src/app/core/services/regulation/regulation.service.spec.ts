import { TestBed } from '@angular/core/testing';

import { RegulationService } from './regulation.service';

describe('RegulationService', () => {
  let service: RegulationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RegulationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
