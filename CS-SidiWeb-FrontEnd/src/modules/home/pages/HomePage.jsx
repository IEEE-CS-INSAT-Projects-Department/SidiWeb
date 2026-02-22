import '../../../styles-tailwind.css'
import { Button } from '../../../shared/components/Button'
import Card from '../../../shared/components/Card'
import ResponsiveGrid from '../../../shared/layout/ResponsiveGrid'

function HomePage() {
	return (
		<main className="min-h-screen bg-vitrine-black1 text-vitrine-white1">
			<section className="max-w-7xl mx-auto px-6 py-4 border-b border-vitrine-grey3">
				<div className="flex items-center justify-between">
					<div className="font-semibold text-base">LOGO</div>
					<nav className="hidden md:flex items-center gap-6 text-sm text-vitrine-grey1">
						<span>Features</span>
						<span>Pricing</span>
						<span>Contact</span>
					</nav>
					<div className="flex items-center gap-3">
						<Button variant="login">Log in</Button>
						<Button variant="signup">Sign up</Button>
					</div>
				</div>
			</section>

			<section className="max-w-7xl mx-auto px-6 py-14">
				<ResponsiveGrid size="L" theme="transparent" width="full">
					<div className="flex flex-col justify-center gap-5">
						<h1 className="text-4xl font-bold leading-tight">
							Sidi Web builds
							<br />
							websites in
							<span className="text-dark-red3"> seconds.</span>
						</h1>
						<p className="text-vitrine-grey1 text-sm max-w-140">
							Prototype statique: remplace ce texte par ton contenu final.
						</p>
						<div className="flex items-center gap-3">
							<Button variant="signup">Get Started</Button>
							<Button variant="demo">Live Demo</Button>
						</div>
					</div>
					<div className="rounded-2xl border border-vitrine-grey3 min-h-65 flex items-center justify-center text-vitrine-grey1">
						Image Placeholder
					</div>
				</ResponsiveGrid>
			</section>

			<section className="max-w-7xl mx-auto px-6 py-12 border-t border-vitrine-grey3">
				<h2 className="text-2xl font-semibold mb-6">From chat to reality</h2>
				<ResponsiveGrid size="L" theme="transparent" width="full">
					<Card variant="dark_step" title="Plan" description="Définir les besoins et objectifs." number="01" icon={<span>•</span>} />
					<Card variant="dark_step" title="Build" description="Assembler les sections principales." number="02" icon={<span>•</span>} />
					<Card variant="dark_step" title="Launch" description="Valider puis livrer la page." number="03" icon={<span>•</span>} />
				</ResponsiveGrid>
			</section>

			<section className="max-w-7xl mx-auto px-6 py-12 border-t border-vitrine-grey3">
				<h2 className="text-2xl font-semibold mb-6">Powerful capabilities</h2>
				<ResponsiveGrid size="XL" theme="transparent" width="full">
					<Card variant="dark_image" title="Smart Generate" description="Placeholder capability card." />
					<Card variant="dark_image" title="Custom Builder" description="Placeholder capability card." />
					<Card variant="dark_image" title="Dark Sync" description="Placeholder capability card." />
					<Card variant="dark_image" title="Deploy Ready" description="Placeholder capability card." />
				</ResponsiveGrid>
			</section>

			<section className="max-w-7xl mx-auto px-6 py-12 border-t border-vitrine-grey3">
				<div className="rounded-[20px] border border-vitrine-grey3 bg-vitrine-black2 p-10 text-center">
					<h3 className="text-3xl font-bold">Ready to build the future?</h3>
					<p className="text-vitrine-grey1 mt-2">Bloc CTA statique à remplacer.</p>
					<div className="mt-6 flex items-center justify-center">
						<Button variant="signup">Start Building</Button>
					</div>
				</div>
			</section>

			<footer className="max-w-7xl mx-auto px-6 py-8 border-t border-vitrine-grey3">
				<div className="text-xs text-vitrine-grey1">Footer placeholder</div>
			</footer>
		</main>
	)
}

export default HomePage
