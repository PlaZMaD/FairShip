// -------------------------------------------------------------------
// -----       Generlal PG source file for SHiP                  -----
// -----      Version as of 0.0.1 by Evgenii Kurbatov            -----
// -----       mailto: ekurbatov(at)hse.ru                       -----
// -------------------------------------------------------------------

#include "TROOT.h"
#include <random>
#include "FairPrimaryGenerator.h"
#include "CosmicsGenerator.h"
#include "TDatabasePDG.h"               // for TDatabasePDG
#include "TMath.h"
#include <boost/json/src.hpp>
#include <G4INCLRandom.hh>

using namespace std;

Bool_t CosmicsGenerator::Init(string mOption){
	pdf_name = 'simple_gauss';
	return kTRUE;
}
// -----   Passing the event   -----------------------------------------
Bool_t CosmicsGenerator::ReadEvent(FairPrimaryGenerator* cpg){

	//Position

	switch(pdf_name){
		case "simple_gauss":
			double sigma = 1.*cm;
			x = G4INCL::Random::gauss(sigma);
			y = G4INCL::Random::gauss(sigma);

		case "flat":
			double range = 1.*cm;
			x = (G4INCL::Random::shoot()-0.5) * range;
			y = (G4INCL::Random::shoot()-0.5) * range;

		case "shifted_gauss":
			double sigma = 1*cm;
			double x_shift = 0.*cm;
			double y_shift = 0.*cm;
			double x_limit = 1.*cm;
			double y_limit = 1.*cm;
			int sample_count = 0;

			while (true){
				x = G4INCL::Random::gauss(sigma) + x_shift;
				y = G4INCL::Random::gauss(sigma) + y_shift;
				if ((TMath::Abs(x) < x_limit) && (TMath::Abs(y) < y_limit)){
					success_flag = true;
					break;
				}
				sample_count++
				if sample_count > 50{
					cout<<"Check your config, too many resamples";
					sample_count = 0;
				}
			}
	}
	//Energy
	switch (energy_distr){
		case "simple":
			px = 0. * GeV;
			py = 0. * GeV;
			pz = 10. * GeV;
	}
	z = -400
	PID = 13;
	TDatabasePDG* pdgBase = TDatabasePDG::Instance();
	mass = pdgBase->GetParticle(PID)->Mass(); // muons!
	weight = 1;

	P = TMath::Sqrt(px*px + py*py + pz*pz);
	cpg->AddTrack(PID,px,py,pz,x,y,z,-1,true,TMath::Sqrt(P*P+mass*mass),0,weight);  // -1 = Mother ID, true = tracking, SQRT(x) = Energy, 0 = t
	return kTRUE;
}
// ---------------------------------------------------------------------

ClassImp(CosmicsGenerator)
